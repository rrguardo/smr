# coding: utf-8

import sys

sys.path.append('..')
from flaskapp.sproxy.nexmo_proxy import nexmo_proxy
from flaskapp import app, mail
from flask_mail import Message

with app.app_context():
    balance = nexmo_proxy().get_balance()
    if balance <= app.config.get("PROXY_BALANCE_THRESHOLD", 1000):
        app.logger.info("WARNING, NEXMO PROXY WITH LOW BALANCE! Balance: %s" % balance)
        msg = Message("WARNING, NEXMO PROXY WITH LOW BALANCE!", ["rrguardo83@gmail.com"],
                      "WARNING, NEXMO PROXY WITH LOW BALANCE! Balance: %s" % balance)
        mail.send(msg)
