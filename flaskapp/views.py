# -*- coding: utf-8 -*-
"""
    flaskapp.views
    ~~~~~~~~~~~~~~

    Main views.
"""

from flask import request, g, render_template, jsonify, url_for
from flaskapp import cache
from flask.ext.babel import gettext
from babelhelper import key_prefix_babelcache
from flask.ext.login import login_required
from flaskapp.models import CountrySmsRate


def index():
    """ Index view"""
    return render_template('home.html', title=gettext('Home Page'))


@cache.cached(timeout=50, key_prefix=key_prefix_babelcache)
def view_cache_per_lang():
    """ Cache and translations ok. """
    return "test"


def api_doc():
    """ api_doc view"""
    api_url = "https://easysms.4simple.org/api/"
    return render_template('api_doc/index.html', api_url=api_url)


def contact():
    """ api_doc view"""
    return render_template('contact.html')


def about():
    """ api_doc view"""
    return render_template('about.html')


@login_required
def demo():
    """ demo view"""
    return render_template('demo.html')


def rates():
    """ rates view"""
    rates = CountrySmsRate.query.all()
    return render_template('rates.html', rates=rates)

