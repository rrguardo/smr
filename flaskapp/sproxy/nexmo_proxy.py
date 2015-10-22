# -*- coding: utf-8 -*-
from flaskapp.sproxy import ProxyInterface
import nexmo


class nexmo_proxy(ProxyInterface):

    def __init__(self):
        # Your Account Sid and Auth Token from nexmo
        self.api_key = '2d0b3be0'
        self.api_secret = '18c94d96'
        self.src = '+12132633701'

    def send(self, to, msg, src=None):
        try:
            if not src:
                src = self.src
            client = nexmo.Client(key=self.api_key, secret=self.api_secret)
            sresult = client.send_message({
                'from': src,
                'to': to,
                'text': msg[:160]
                })
            return sresult
        except:
            pass
        return False

    def get_balance(self):
        return -1