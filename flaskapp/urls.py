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

