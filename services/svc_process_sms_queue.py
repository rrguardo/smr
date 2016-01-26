# coding: utf-8

import sys
import json
sys.path.append('..')

from flaskapp import db
from flaskapp.models import SMS_Status
from flaskapp.sproxy.tw_proxy import tw_proxy
from flaskapp.sproxy.plivo_proxy import plivo_proxy
from flaskapp.sproxy.nexmo_proxy import nexmo_proxy
from flaskapp.settings import Config
import pika


PROXYS = [{"class": tw_proxy, "fails": 0, "enabled": False},
    {"class": plivo_proxy, "fails": 0, "enabled": False},
    {"class": nexmo_proxy, "fails": 0, "enabled": True}]


def proxy_pick():
    """Pick one enabled proxy with less fails."""
    prox_enabled = [item for item in PROXYS if item.get("enabled", False)]
    result = prox_enabled[0]
    for prox in prox_enabled:
        if prox["fails"] < result["fails"]:
            result = prox
    return result.get("class")


def proxy_inc_fails(class_inst):
    for prox in PROXYS:
        if prox["class"] == class_inst:
            prox["fails"] = prox["fails"] + 1


def queue_callback(ch, method, properties, body):
    try:
        print " [x] Received %r" % (body,)
        job = json.loads(body)
        to_ = job.get("to")
        message_ = job.get("message")
        pid = job.get("pid")

        sm = SMS_Status.query.filter_by(id=pid).first()
        sm.status = "processing"
        db.session.add(sm)
        db.session.commit()

        sprox = proxy_pick()
        sresult = sprox().send(to_, message_)
        if not sresult:
            proxy_inc_fails(sprox)
            print "SMS Proxy %s fails" % sprox.__name__
            sm.status = "failed-r1"
            db.session.add(sm)
            db.session.commit()
        else:
            sm.status = "success-delivered"
            db.session.add(sm)
            db.session.commit()
    except:
        print "error in queue processing"


def process_sms_queue():
    credentials = pika.PlainCredentials(Config.RABBIT_USER, Config.RABBIT_PASSW)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Config.RABBIT_HOST, port=Config.RABBIT_PORT, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='sms')
    channel.basic_consume(queue_callback, queue='sms', no_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    process_sms_queue()
