# -*- coding: utf-8 -*-
"""
    flaskapp.settings
    ~~~~~~~~~~~~~~~~~

    Flask application settings.

    Mandril settings:
    email: admin@4simple.org
    passw: #CvTs8v*SL

    Host smtp.mandrillapp.com
    Port 587
    SMTP Username: admin@4simple.org
    SMTP Password: B-mP6-lh9Nx71OWqybkM4g
"""


class Config(object):
    """ Configuration base class"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:1234567*@127.0.0.1/smr'
    SECRET_KEY = 'development key'
    #LOG SETTINGS
    LOG_EML_ADMINS = ['yourname@example.com']
    LOG_EML_SENDER = 'server-error@example.com'
    LOG_SMTP_SRV = '127.0.0.1'
    LOG_FILE = 'flaskapp.log'
    #BABEL CONFIG
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    #All files cache headers
    SEND_FILE_MAX_AGE_DEFAULT = 60 * 60 * 12  # 12 hours def value
    #RECAPTCHA
    RECAPTCHA_PUBLIC_KEY = '6LcIsRMTAAAAAIpUA83BM9kD9AJpQTzh3qhqfwIF'
    RECAPTCHA_PRIVATE_KEY = '6LcIsRMTAAAAABctHcyKQbM0-_cYerIUc3UGQ3dA'

    MAIL_SERVER = 'smtp.mandrillapp.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'admin@4simple.org'
    MAIL_PASSWORD = 'B-mP6-lh9Nx71OWqybkM4g'
    MAIL_DEFAULT_SENDER = 'noreply@4simple.org'



class ProductionConfig(Config):
    """ Configuration for production stage"""
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:1234567*@127.0.0.1/smr'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'
    #LOG_FILE = '/home/appuser/flaskdeploy/flaskapp.log'


class DevelopmentConfig(Config):
    """ Configuration for development stage"""
    DEBUG = True


class TestingConfig(Config):
    """ Configuration for testing stage"""
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:1234567*@127.0.0.1/smr'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'
    #LOG_FILE = '/home/appuser/flaskdeploy/flaskapp.log'

