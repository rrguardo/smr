# -*- coding: utf-8 -*-
"""
    flaskapp.store.models
    ~~~~~~~~~~~~~~
    
    SQLAlchemy user models.
"""


from flaskapp import db
import datetime


class PayPalIPN(db.Model):
    """ Paypal IPN transactions model"""
    id = db.Column(db.Integer, primary_key=True)
    txnid = db.Column(db.String(20), unique=True, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(25), nullable=False)
    item_name = db.Column(db.String(50), nullable=False)
    receiver_email = db.Column(db.String(50), nullable=False)
    payer_email = db.Column(db.String(50), nullable=False)
    custom = db.Column(db.Integer)
    itemid = db.Column(db.String(25), nullable=False)
    createdtime = db.Column(db.DateTime)

    def __init__(self, data):
        self.txnid = data.get("txnid")
        self.payment_amount = data.get("payment_amount")
        self.payment_status = data.get("payment_status")
        self.item_name = data.get("item_name")
        self.receiver_email = data.get("receiver_email")
        self.payer_email = data.get("payer_email")
        self.custom = data.get("custom")
        self.itemid = data.get("itemid")
        self.createdtime = data.get("createdtime")
