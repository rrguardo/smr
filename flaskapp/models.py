# -*- coding: utf-8 -*-
"""
    flaskapp.model
    ~~~~~~~~~~~~~~

    SQLAlchemy database models.
"""

from flaskapp import db
from sqlalchemy.sql import func


class CountrySmsRate(db.Model):
    """ System rate model"""
    __tablename__ = 'country_sms_rate'

    country_cd = db.Column(db.String(2), primary_key=True)
    prefix = db.Column(db.String(5), primary_key=True)
    country_name = db.Column(db.String(40))
    base_rate = db.Column(db.Float)
    fix_rate = db.Column(db.Float)
    insert_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)


class SMS_Status(db.Model):
    """ table for track sms status."""
    __tablename__ = 'SMS__status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    user_id = db.Column(db.Integer)
    send_date = db.Column(db.DateTime, default=func.now())
    proxy = db.Column(db.Integer)
    proxy_msg_id = db.Column(db.String(150))
    proxy_status = db.Column(db.String(50))

    def __init__(self, user_id, status):
        self.user_id = user_id
        self.status = status
