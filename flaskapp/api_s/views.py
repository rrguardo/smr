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
from flaskapp import db, app
from flaskapp.utils.rate import out_sms_rate
import beanstalkc


class Auth_API:
    """Base class for auth API usage."""

    def __init__(self):
        self._user = None

    def auth_user(self):
        try:
            auth_token = request.form.get('auth_token', "")
            user_id = request.form.get('user_id', "")
            self._user = User.query.filter_by(id=user_id, auth_token=auth_token).first()
        except Exception, e:
            app.logger.error("auth-error: %s" % e.message)
            app.logger.error("auth-error uid: %s tk: %s" % (user_id, auth_token))
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
            except Exception, e:
                app.logger.error("get_sms_status: %s" % e.message)
                return jsonify({'error': 'Pid error'})
        else:
            return jsonify({'error': 'Login error'})

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
                return jsonify({'error': 'Message with more than 160 chars'})
            rate_ = out_sms_rate(to_)
            if rate_ <= 0:
                return jsonify({'error': 'Invalid phone number format.'})
            if rate_ > 0 and rate_ < self._user.balance:
                # discount balance before send sms
                User.update_user_balance(self._user.id, rate_*-1)
                st = SMS_Status(self._user.id, 'queued')
                db.session.add(st)
                db.session.commit()
                sms_job = {'to': to_,
                           'message': message_,
                           'pid': st.id,
                           'user_id': self._user.id,
                           'rate': rate_}
                sms_job = json.dumps(sms_job)
                if not process_sms(sms_job):
                    return jsonify({'error': 'queue error'})
                return jsonify({'success': 'ok', 'pid': st.id})
            else:
                return jsonify({'error': 'Low balance'})
        else:
            return jsonify({'error': 'Login error'})


def process_sms(sms_job):
    """Process the sms"""
    try:
        beanstalk = beanstalkc.Connection(host=app.config.get('BEANSTALK_HOST'),
                                          port=app.config.get('BEANSTALK_PORT'))
        beanstalk.use('sms')
        beanstalk.put(sms_job)
        beanstalk.close()
    except Exception as ex:
        app.logger.exception("process_sms fails: %s", ex)
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
