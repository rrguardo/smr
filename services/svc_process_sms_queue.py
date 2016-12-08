# coding: utf-8

import sys
import json
import logging
sys.path.append('..')

from flaskapp import db, app
from flaskapp.models import SMS_Status
from flaskapp.user.models import User
from flaskapp.sproxy.tw_proxy import tw_proxy
from flaskapp.sproxy.plivo_proxy import plivo_proxy
from flaskapp.sproxy.nexmo_proxy import nexmo_proxy
from flaskapp.settings import Config
import beanstalkc


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
            prox["fails"] += 1


def queue_callback(body):
    try:
        logging.info(" [x] Received %s", body)
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
            app.logger.error("SMS Proxy %s fails" % sprox.__name__)
            sm.status = "failed-r1"
            db.session.add(sm)
            db.session.commit()
        else:
            sm.status = "success-delivered"
            sm.proxy = str(sprox.proxy_id)
            if isinstance(sresult, dict):
                sm.proxy_msg_id = str(sresult.get("msg_id"))
                sm.proxy_status = str(sresult.get("status"))
                # add future refunds or extra discounts here
                if sresult.get("total", 1) > 1:
                    User.update_user_balance(sm.user_id, sm.rate*-1)
            db.session.add(sm)
            db.session.commit()
    except Exception, e:
        logging.exception("error in queue processing: %s" % e.message)


def process_sms_queue():
    beanstalk = beanstalkc.Connection(host=Config.BEANSTALK_HOST, port=Config.BEANSTALK_PORT)
    beanstalk.use('sms')
    while True:
        job = beanstalk.reserve()
        body = job.body
        job.delete()
        if body:
            # TODO: this function should be called asynchronous
            queue_callback(body)


if __name__ == "__main__":
    process_sms_queue()
