# -*- coding: utf-8 -*-
"""
    flaskapp.api.views
    ~~~~~~~~~~~~~~~~~~~~

    API RESTFUL views here.
"""

import json
from flask import jsonify, request
from flaskapp.user.models import User
from flaskapp.models import SMS_Status
from flaskapp import db
from flaskapp.utils.rate import out_sms_rate
import pika


class Auth_API:
    """Base class for auth API usage."""

    def __init__(self):
        self._user = None

    def auth_user(self):
        try:
            auth_token = request.form['auth_token']
            user_id = request.form['user_id']
            self._user = User.query.filter_by(id=user_id,
                auth_token=auth_token).first()
        except:
            self._user = None
        finally:
            return self._user is not None

    def get_balace(self):
        """
        Get user Balance:
            user_id
            auth_token
        """
        if self.auth_user():
            return jsonify({'balance': self._user.balance})
        else:
            return jsonify({'error': 'login-error'})

    def get_sms_status(self):
        """
        Get sms status:
            user_id
            auth_token
            pid
        """
        if self.auth_user():
            try:
                pid = request.form['pid']
                sm = SMS_Status.query.filter_by(id=pid,
                    user_id=self._user.id).first()
                return jsonify({'status': sm.status})
            except:
                return jsonify({'error': 'pid error'})
        else:
            return jsonify({'error': 'login-error'})

    def send_sms(self):
        """
        API Send SMS:
            user_id
            auth_token
            to
            body

        Body should be <= 160 chars
        """
        if self.auth_user():
            to_ = request.form.get('to', False)
            if not to_:
                return jsonify({'error': 'Destination number required!'})
            message_ = request.form.get('body', False)
            if not message_:
                return jsonify({'error': 'Message required!'})
            if len(message_) > 160:
                return jsonify({'error': 'message with more than 160 chars'})
            rate_ = out_sms_rate(to_)
            if rate_ <= 0:
                return jsonify({'error': 'invalid phone number format.'})
            if rate_ > 0 and rate_ < self._user.balance:
                # discount balance before send sms
                db.engine.execute("""UPDATE user
                    SET balance = balance-%s
                    WHERE id = %s
                    """ % (rate_, self._user.id))
                st = SMS_Status(self._user.id, 'queued')
                db.session.add(st)
                db.session.commit()
                sms_job = {'to': to_, 'message': message_, 'pid': st.id}
                sms_job = json.dumps(sms_job)
                if not process_sms(sms_job):
                    return jsonify({'error': 'queue error'})
                return jsonify({'success': 'message delivered', 'pid': st.id})
            else:
                return jsonify({'error': 'low balance'})
        else:
            return jsonify({'error': 'login-error'})


def process_sms(sms_job):
    """Process the sms"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sms')
        channel.basic_publish(exchange='', routing_key='sms', body=sms_job)
        connection.close()
    except:
        return False
    return True


def get_balance():
    api = Auth_API()
    return api.get_balace()


def send_sms():
    api = Auth_API()
    return api.send_sms()


def get_sms_status():
    api = Auth_API()
    return api.get_sms_status()
