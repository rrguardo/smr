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
url(app, '/_add_numbers', 'views.add_numbers')
url(app, '/api_documentation', 'views.api_doc')
url(app, '/contact', 'views.contact')
url(app, '/about', 'views.about')
url(app, '/demo', 'views.demo')
url(app, '/rates', 'views.rates')
