# -*- coding: utf-8 -*-
"""
    flaskapp.user.urls
    ~~~~~~~~~~~~~~~~~~~

    Add all url <-> view maps here for user sub-package.
"""


from flaskapp.store import store_bp
from flaskapp.store.views import *


store_bp.add_url_rule('/paypal_ipn', 'paypal_ipn', paypal_ipn)
store_bp.add_url_rule('/success.html', 'success', success)
store_bp.add_url_rule('/cancel.html', 'cancel', cancel)
