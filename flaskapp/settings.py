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

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    #MAIL_USERNAME = 'noreply@4simple.org'
    #MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'noreply@4simple.org'
    # Flask-User settings
    USER_ENABLE_CHANGE_USERNAME = False
    USER_APP_NAME = 'EasySMS'
    USER_AFTER_LOGIN_ENDPOINT = 'user.panel'
    USER_AFTER_CONFIRM_ENDPOINT = 'user.panel'
    USER_AFTER_CHANGE_PASSWORD_ENDPOINT = 'user.panel'
    USER_AFTER_RESET_PASSWORD_ENDPOINT = 'user.panel'
    # flask cache conf
    CACHE_TYPE = 'simple'
    # only enable api
    IS_API = False


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

