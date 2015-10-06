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

def add_numbers():
    """ JQuery test view"""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

