# -*- coding: utf-8 -*-
"""
    flaskapp.user.views
    ~~~~~~~~~~~~~~~~~~~~

    User views here.
"""

from urllib import urlopen, urlencode, quote_plus
import werkzeug.datastructures
import flask
from flaskapp import db, app
from flaskapp.user.models import User
from flaskapp.store.models import PayPalIPN
from sqlalchemy import and_
from itertools import chain
from flask import request, g, redirect, url_for, render_template,\
    flash, jsonify
from flaskapp.store.paddle import verify as paddle_verify


IPN_URLSTRING = 'https://www.paypal.com/cgi-bin/webscr'
IPN_VERIFY_EXTRA_PARAMS = (('cmd', '_notify-validate'),)


def ordered_storage(f):
    def decorator(*args, **kwargs):
        flask.request.parameter_storage_class = \
            werkzeug.datastructures.ImmutableOrderedMultiDict
        return f(*args, **kwargs)
    return decorator


def validation_basic(txn_id, payment_status, mc_currency,
        receiver_email, mc_gross, item_num):
    if payment_status == "Completed" and mc_currency == "USD" and \
            receiver_email == "sales@4simple.org" and mc_gross > 0 and \
            item_num == '578' and \
            PayPalIPN.query.filter(PayPalIPN.txnid == txn_id).count() == 0:
        return True
    return False


@ordered_storage
def paypal_ipn():
    """"PayPal IPN processing."""
    verify_args = chain(request.form.iteritems(), IPN_VERIFY_EXTRA_PARAMS)
    verify_string = '&'.join(('%s=%s' % (param, value)
        for param, value in verify_args))
    response = urlopen(IPN_URLSTRING, data=verify_string)
    status = response.read()
    if status == 'VERIFIED':
        # Processing verified transaction details.
        payment_status = request.form.get('payment_status')
        txn_id = request.form.get('txn_id')
        receiver_email = request.form.get('receiver_email')
        mc_gross = float(request.form.get('mc_gross'))
        mc_fee = float(request.form.get('mc_fee'))
        mc_currency = request.form.get('mc_currency')
        custom = int(request.form.get('custom'))
        item_num = '578'  # str(request.form.get('item_number'))
        if validation_basic(txn_id, payment_status, mc_currency,
            receiver_email, mc_gross, item_num):
            ipn_rec = PayPalIPN(request.form)
            db.session.add(ipn_rec)
            db.session.commit()
            # Updating balance
            usr = User.query.filter_by(id=custom).first()
            usr.update_balance(mc_gross - mc_fee)
            app.logger.info("Success payment txn_id: %s " % txn_id)
        else:
            app.logger.error("validation_basic fails txn_id: %s " % txn_id)
    else:
        app.logger.error('Paypal IPN string {arg} did not validate'.format(
             arg=verify_string))
    return jsonify({'status': 'complete'})


def success():
    """PayPal IPN success page"""
    return render_template("store/success.html")


def cancel():
    """PayPal IPN success page"""
    return render_template("store/cancel.html")


def paddle_ipn():
    app.logger.warning(request.data)
    app.logger.warning(request.form)
    if paddle_verify(request.form):
        app.logger.warning("Paddle verify success")
    else:
        app.logger.warning("Paddle verify fail")
    return "OK"


def bitcoinpay_ipn():
    app.logger.warning(request.data)
    app.logger.warning("++++++++++++++++++++++++++++++")
    app.logger.warning(request.form)
    return "OK"
