# -*- coding: utf-8 -*-
"""
    flaskapp.settings
    ~~~~~~~~~~~~~~~~~

    Flask application settings.
"""


class Config(object):
    """ Configuration base class"""
    DEBUG = False
    TESTING = False
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////home/appuser/flaskdeploy/flask.db'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234567*@127.0.0.1/smr'
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
    RECAPTCHA_PUBLIC_KEY = 'recaptcha public key'


class ProductionConfig(Config):
    """ Configuration for production stage"""
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234567*@127.0.0.1/smr'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////home/appuser/flaskdeploy/flask.db'
    #LOG_FILE = '/home/appuser/flaskdeploy/flaskapp.log'


class DevelopmentConfig(Config):
    """ Configuration for development stage"""
    DEBUG = True


class TestingConfig(Config):
    """ Configuration for testing stage"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234567*@127.0.0.1/smr'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////home/appuser/flaskdeploy/flask.db'
    #LOG_FILE = '/home/appuser/flaskdeploy/flaskapp.log'

