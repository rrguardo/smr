# -*- coding: utf-8 -*-
"""
    flaskapp.admin.urls
    ~~~~~~~~~~~~~~~~~~~

    Add all url <-> view maps here for admin sub-package.
"""


from flaskapp.lazyhelpers import url
from flaskapp import app


url(app, '/balance', 'api_s.views.get_balance', methods=['POST'])
url(app, '/sms', 'api_s.views.send_sms', methods=['POST'])
url(app, '/status', 'api_s.views.get_sms_status', methods=['POST'])
