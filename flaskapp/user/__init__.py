# -*- coding: utf-8 -*-
"""
    flaskapp.user
    ~~~~~~~~~~~~~~

    User package here.
"""

from flask import Blueprint


user_bp = Blueprint('user', __name__, template_folder='templates',
            static_folder='static')

#Loding url<->views
import flaskapp.user.urls
