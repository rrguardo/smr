# -*- coding: utf-8 -*-
"""
    flaskapp.views
    ~~~~~~~~~~~~~~

    Main views.
"""

from flask import request, g, render_template, jsonify, url_for, flash, redirect
from flaskapp import cache, mail
from flask.ext.babel import gettext
from babelhelper import key_prefix_babelcache
from flask.ext.login import login_required, current_user
from flaskapp.models import CountrySmsRate
from flaskapp.forms import ContactForm
from flask_mail import Message


def index():
    """ Index view"""
    return render_template('home.html', title=gettext('Home Page'))


@cache.cached(timeout=50, key_prefix=key_prefix_babelcache)
def view_cache_per_lang():
    """ Cache and translations ok. """
    return "test"


def api_doc():
    """ api_doc view"""
    api_url = "https://api.4simple.org/"
    return render_template('api_doc/index.html', api_url=api_url)


def contact():
    """ api_doc view"""
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        usr_info = ""
        if not current_user.is_anonymous:
            usr_info = "current_user id: %s \n <br>" % current_user.id
        msg = Message("CONTACT EasySMS: " + form.subject.data,
                      ["rrguardo83@gmail.com"],
                      usr_info + form.message.data)
        mail.send(msg)
        flash('Request submitted successfully, thanks for your feedback.')
        return render_template('contact.html', form=False)
    return render_template('contact.html', form=form)


def tos():
    """ tos view"""
    return render_template('tos.html')


@login_required
def demo():
    """ demo view"""
    return render_template('demo.html')


@cache.cached(timeout=3600)
def get_rates():
    """ get rates from cache."""
    return CountrySmsRate.query.all()


def rates():
    """ rates view, 1 hour cache"""
    return render_template('rates.html', data=get_rates())

