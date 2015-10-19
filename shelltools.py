# -*- coding: utf-8 -*-
"""
    Flaskapp Shell Utils Script
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flaskapp shell functions utils here.

"""

from flaskapp import app, db
from sys import argv


def init_context(ctx):
    """ Init shell with context """
    ctx = app.test_request_context()
    ctx.push()
    app.preprocess_request()

def shutdown_request(ctx):
    """ Process the response and shutdown the context """
    app.process_response(app.response_class())
    ctx.pop()

def test_shell(ctx):
    """ Test server shell"""
    init_context(ctx)
    shutdown_request(ctx)

def init_database():
    """ Create database using sqlalchemy Model"""
    db.create_all()
    # inserting some test data
    from flaskapp.user.models import User
    admin = User('admin', 'admin@example.com', 
                 '2ea6201a068c5fa0eea5d81a3863321a87f8d533')
    guest = User('guest', 'guest@example.com', 
                 '2ea6201a068c5fa0eea5d81a3863321a87f8d533')
    guest.auth_token = "1234567"
    guest.balance = 100
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    users = User.query.all()
    print users
