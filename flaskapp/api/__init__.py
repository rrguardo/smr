# -*- coding: utf-8 -*-
"""
    flaskapp.admin
    ~~~~~~~~~~~~~~

    Admin package here.
"""

from flask import Blueprint


api_bp = Blueprint('api', __name__)

# Views import here >>
#lazy-optimized views load
import flaskapp.api.urls
