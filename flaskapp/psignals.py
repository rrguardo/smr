# -*- coding: utf-8 -*-
"""
    flaskapp.psignals
    ~~~~~~~~~~~~~~~~~

    Main signals processing.
"""

from flask.ext.user import user_registered
from flaskapp import app, db


@user_registered.connect_via(app)
def _after_register_hook(sender, user, **extra):
    user.update_token()
    db.session.commit()
