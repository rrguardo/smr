# -*- coding: utf-8 -*-
"""
    flaskapp.epages
    ~~~~~~~~~~~~~~~
    
    Page error handlers: 404, 410, 403, ...
"""

from flask import render_template
from flaskapp import app

@app.errorhandler(404)
def page_not_found(e):
    """ Resources not found"""
    return render_template('epages/404.html'), 404

@app.errorhandler(410)
def page_gone(e):
    """ Resources that previously existed and got deleted """
    return render_template('epages/410.html'), 410

@app.errorhandler(403)
def page_forbidden(e):
    """ Not right to access the page"""
    return render_template('epages/403.html'), 403
