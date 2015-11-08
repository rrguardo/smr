# -*- coding: utf-8 -*-
from flaskapp.sproxy import ProxyInterface
from twilio.rest import TwilioRestClient


class tw_proxy(ProxyInterface):

    def __init__(self):
        # Your Account Sid and Auth Token from twilio.com/user/account
        self._account_sid = "AC94b03a2913bd39d854393b9514eea189"
        self._auth_token = "39db55f01cb8d0797944ab58f9035eac"
        self.src = "+17064384160"
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
        except Exception, ex:
            print str(ex)
        return False

    def get_balance(self):
        return -1
