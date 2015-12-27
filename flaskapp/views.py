# -*- coding: utf-8 -*-
"""
    flaskapp.views
    ~~~~~~~~~~~~~~

    Main views.
"""

from flask import request, g, render_template, jsonify
from flaskapp import cache
from flask.ext.babel import gettext
from babelhelper import key_prefix_babelcache


def index():
    """ Index view"""
    return render_template('home.html', title=gettext(u'Home Page'))


@cache.cached(timeout=50, key_prefix=key_prefix_babelcache)
def view_cache_per_lang():
    """ Cache and translations ok. """
    return "test"


def api_doc():
    """ api_doc view"""
    return render_template('api_doc/index.html')


def contact():
    """ api_doc view"""
    return render_template('contact.html')


def about():
    """ api_doc view"""
    return render_template('about.html')
