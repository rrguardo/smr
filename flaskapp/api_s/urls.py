# -*- coding: utf-8 -*-
"""
    flaskapp.admin.urls
    ~~~~~~~~~~~~~~~~~~~

    Add all url <-> view maps here for admin sub-package.
"""


from flaskapp.lazyhelpers import url
from flaskapp.api_s import api_s_bp


url(api_s_bp, '/balance', 'api_s.views.get_balance', methods=['POST'])
url(api_s_bp, '/sms', 'api_s.views.send_sms', methods=['POST'])
