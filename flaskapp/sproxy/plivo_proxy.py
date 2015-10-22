# -*- coding: utf-8 -*-
from flaskapp.sproxy import ProxyInterface
import plivo


class plivo_proxy(ProxyInterface):

    def __init__(self):
        # Your Account Sid and Auth Token from plivo
        self.auth_id = 'MAMTGYOWYWMGU5YWZLNZ'
        self.auth_token = 'OWFiM2M0NWY2MWQ1MzY1MDBhMGFjYmRhYmY1M2Vm'
        self.src = '+14158141829'

    def send(self, to, msg, src=None):
        try:
            if not src:
                src = self.src
            client = plivo.RestAPI(self.auth_id, self.auth_token)
            message = client.Message.send(
                src=src,
                dst=to,
                text=msg[:160]
            )
            return message
        except:
            pass
        return False

    def get_balance(self):
        return -1