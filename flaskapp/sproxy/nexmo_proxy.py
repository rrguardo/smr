# -*- coding: utf-8 -*-
from flaskapp.sproxy import ProxyInterface
from flaskapp import app
import nexmo


class nexmo_proxy(ProxyInterface):
    """
     nexmo sms proxy
    """
    proxy_id = 0

    def __init__(self):
        # Your Account Sid and Auth Token from nexmo
        self.api_key = '2d0b3be0'
        self.api_secret = '18c94d96'
        self.src = '+12132633701'

    def _parse(self, response):
        """
        :param response: request response
        :return: update status.
        """""
        try:
            total = len(response['messages'])
            total_ok = 0
            msg_id = ""
            status = ""
            for msg in response['messages']:
                if msg['status'] == 0:
                    total_ok = total_ok + 1
                status = status + str(msg["status"]) + ","
                msg_id = msg_id + str(msg["message-id"]) + ","
            return (total, total_ok, msg_id, status)
        except Exception, e:
            app.logger.error("Error parsing nexmo response: %s" % e.message)
            return (1, 0, "000", "000")

    def send(self, to, msg, src=None):
        try:
            if not src:
                src = self.src
            client = nexmo.Client(key=self.api_key, secret=self.api_secret)
            response = client.send_message({
                'from': src,
                'to': to,
                'text': msg
                })
            parsed = self._parse(response)
            return {"success": parsed[0] == parsed[1],
                    "msg_id": parsed[2],
                    "total": parsed[0],
                    "status": parsed[3]}
        except Exception, e:
            app.logger.error("Error parsing sending sms: %s" % e.message)
        return False

    def get_balance(self):
        try:
            client = nexmo.Client(key=self.api_key, secret=self.api_secret)
            return float(client.get_balance()['value'])
        except Exception, e:
            app.logger.error("Nexmo get balance error: %s" % e.message)
