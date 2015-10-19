# coding: utf-8

import sys
import json
sys.path.append('..')

from flaskapp import db
from flaskapp.models import SMS_Status
import pika


def queue_callback(ch, method, properties, body):
    try:
        print " [x] Received %r" % (body,)
        job = json.loads(body)
        sm = SMS_Status.query.filter_by(id=job.get('pid', False)).first()
        sm.status = "processing"
        db.session.add(sm)
        db.session.commit()
    except:
        print "error in queue processing"


def process_sms_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sms')
    channel.basic_consume(queue_callback, queue='sms', no_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    process_sms_queue()
