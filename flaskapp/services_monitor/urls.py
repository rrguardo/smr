# -*- coding: utf-8 -*-
"""
    flaskapp.user.urls
    ~~~~~~~~~~~~~~~~~~~

    Add all url <-> view maps here for user sub-package.
"""


from flaskapp.services_monitor import monitor_bp
from flaskapp.services_monitor.views import *


monitor_bp.add_url_rule('/cache', 'cache', monitor_cache, methods=['POST', 'GET'])
