# -*- coding: utf-8 -*-
"""
    flaskapp.admin
    ~~~~~~~~~~~~~~

    Admin package here.
"""

from flask import Blueprint


api_s_bp = Blueprint('api_s', __name__)

# Views import here >>
#lazy-optimized views load
import flaskapp.api_s.urls
