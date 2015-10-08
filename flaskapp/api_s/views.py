# -*- coding: utf-8 -*-
"""
    flaskapp.api.views
    ~~~~~~~~~~~~~~~~~~~~

    API RESTFUL views here.
"""

import json
from flask import Flask, g, jsonify, render_template, request, abort
from flaskapp.user.models import User
from flaskapp import db, cache


class Auth_API:
    """Base class for auth API usage."""

    def __init__(self):
        self._user = None

    def auth_user(self):
        try:
            auth_token = request.form['auth_token']
            user_id = request.form['user_id']
            self._user = User.query.filter_by(id=user_id,
                auth_token=auth_token).first()
        except:
            self._user = None
        finally:
            return self._user is not None

    def get_balace(self):
        if self.auth_user():
            return jsonify({'balance': self._user.get('balance', 0)})
