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
