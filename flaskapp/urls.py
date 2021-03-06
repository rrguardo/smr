# -*- coding: utf-8 -*-
"""
    flaskapp.urls
    ~~~~~~~~~~~~~

    Add all url <-> view maps.
"""

from flaskapp.lazyhelpers import url
from flaskapp import app


#Set all lazy-optimized views here >>>
url(app, '/', 'views.index')
url(app, '/api_documentation', 'views.api_doc')
url(app, '/contact', 'views.contact', methods=["GET", "POST"])
url(app, '/tos', 'views.tos')
url(app, '/demo', 'views.demo')
url(app, '/rates', 'views.rates')
