# -*- coding: utf-8 -*-
"""
    flaskapp.settings
    ~~~~~~~~~~~~~~~~~

    Flask application settings.
"""

import os


class Config(object):
    """ Configuration base class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'xVuTBn74F9VhTy62SaLy5p0TxCrJP51062Cc33'
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
    MAIL_USERNAME = 'noreply'
    #MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'noreply@4simple.org'
    # Flask-User settings
    USER_ENABLE_CHANGE_USERNAME = False
    USER_APP_NAME = 'EasySMS'
    USER_AFTER_LOGIN_ENDPOINT = 'user.panel'
    USER_AFTER_CONFIRM_ENDPOINT = 'user.panel'
    USER_AFTER_CHANGE_PASSWORD_ENDPOINT = 'user.panel'
    USER_AFTER_RESET_PASSWORD_ENDPOINT = 'user.panel'
    # rabbitmq settings
    RABBIT_USER = "smrxcdsfsx"
    RABBIT_PASSW = "HvRh62Vc38VcTsKhTT31S"
    RABBIT_HOST = "localhost"
    RABBIT_PORT = 5672
    # only enable api
    IS_API = False
    if os.environ.get("IS_API", False):
        IS_API = True
    # sms proxy balance threshold
    PROXY_BALANCE_THRESHOLD = 5


class ProductionConfig(Config):
    """ Configuration for production stage"""
    # database conf.
    SQLALCHEMY_DATABASE_URI = 'mysql://root:c5XwpgT71CvvTs3Sd@127.0.0.1/smr'
    # flask cache conf
    CACHE_TYPE = 'memcached'
    CACHE_DEFAULT_TIMEOUT = 60
    CACHE_MEMCACHED_SERVERS = ['127.0.0.1']


class DevelopmentConfig(Config):
    """ Configuration for development stage"""
    DEBUG = True
    CACHE_TYPE = 'simple'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'


class TestingConfig(Config):
    """ Configuration for testing stage"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'
    CACHE_TYPE = 'simple'
