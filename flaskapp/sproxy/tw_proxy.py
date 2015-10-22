# -*- coding: utf-8 -*-
from flaskapp.sproxy import ProxyInterface
from twilio.rest import TwilioRestClient


class tw_proxy(ProxyInterface):

    def __init__(self):
        # Your Account Sid and Auth Token from twilio.com/user/account
        self._account_sid = "AC05dcefb0263c059a49047298d2a88ccf"
        self._auth_token = "ce6510c4650f03a34d63bfa5a3ebadee"
        self.src = "+17607849554"
        # phone sid PNe8fbd81576ad24ee5636156de339462a

    def send(self, to, msg, src=None):
        try:
            if not src:
                src = self.src
            client = TwilioRestClient(self._account_sid, self._auth_token)
            message = client.messages.create(
                body=msg[:160],
                to=to,
                from_=src)
            return message
        except:
            pass
        return False

    def get_balance(self):
        return -1