# -*- coding: utf-8 -*-
"""
    flaskapp.user.views
    ~~~~~~~~~~~~~~~~~~~~

    User views here.
"""

from urllib import urlopen, urlencode, quote_plus
import werkzeug.datastructures
import flask
from flaskapp import db
from flaskapp.user.models import User
from sqlalchemy import and_
from itertools import chain
from flask import request, g, redirect, url_for, render_template,\
    flash, jsonify


IPN_URLSTRING = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
# IPN_URLSTRING = 'https://www.paypal.com/cgi-bin/webscr'
IPN_VERIFY_EXTRA_PARAMS = (('cmd', '_notify-validate'),)


def ordered_storage(f):
    def decorator(*args, **kwargs):
        flask.request.parameter_storage_class = \
            werkzeug.datastructures.ImmutableOrderedMultiDict
        return f(*args, **kwargs)
    return decorator


@ordered_storage
def paypal_ipn():
    """"PayPal IPN processing."""
    verify_args = chain(request.form.iteritems(), IPN_VERIFY_EXTRA_PARAMS)
    verify_string = '&'.join(('%s=%s' % (param, value) for param, value in verify_args))
    #req = Request(verify_string)
    response = urlopen(IPN_URLSTRING, data=verify_string)
    status = response.read()
    print status
    if status == 'VERIFIED':
        print "PayPal transaction was verified successfully."
        # Do something with the verified transaction details.
        payer_email =  request.form.get('payer_email')
        print "Pulled {email} from transaction".format(email=payer_email)
    else:
         print 'Paypal IPN string {arg} did not validate'.format(arg=verify_string)

    return jsonify({'status':'complete'})