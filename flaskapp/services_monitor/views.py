# -*- coding: utf-8 -*-
"""
"""


from flask import request, g, render_template, jsonify, url_for, flash, redirect
from flaskapp import cache, mail


def monitor_cache():
    """ Index view"""
    return render_template('services_monitor/status.html', service_name='cache', service_status="OK")

def monitor_user():
    hdrs = request.headers
    return render_template('services_monitor/user.html', headers=hdrs)
