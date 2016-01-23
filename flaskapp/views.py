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
from flask.ext.login import login_required
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
    api_url = "https://easysms.4simple.org/api/"
    return render_template('api_doc/index.html', api_url=api_url)


def contact():
    """ api_doc view"""
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        msg = Message("CONTACT EasySMS: " + form.subject.data,
                      ["support@4simple.org"],
                      form.message.data)
        mail.send(msg)
        flash('Request submitted successfully, thanks for your feedback.')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


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
    return render_template('rates.html', data=rates)

