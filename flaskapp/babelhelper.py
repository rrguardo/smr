# -*- coding: utf-8 -*-
"""
    flaskapp.babelhelper
    ~~~~~~~~~~~~~~~~~~~~

    Helper for babel support.
"""

from flask import g, request
from flaskapp import babel
from flask.ext.babel import get_locale as get_locale_ex


@babel.localeselector
def get_locale():
    """ Get the g.user.locale language code, 
        otherwise try get language code using browser header.
    """
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits. We support en/es in this
    # example. The best match wins.
    return request.accept_languages.best_match(['en','es'])

@babel.timezoneselector
def get_timezone():
    """ Get the user.timezone else otherwise use default timezone."""
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
    return None

def key_prefix_babelcache():
    """ Patch to support babel and cache.
    Replace views cache default key_prefix using this function.
    
    Usage::
        
        #file views.py
        from babelhelper import key_prefix_babelcache
        ...
        
        @cache.cached(timeout=50, key_prefix=key_prefix_babelcache)
        def index():
            ...
    """
    return str(get_locale_ex()) + 'view/%s'

