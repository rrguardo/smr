# -*- coding: utf-8 -*-
"""
    flaskapp
    ~~~~~~~~

    A microblog base application using Flask and SQLAlchemy.
    
    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

__version__ = '0.1'

from gettext import gettext as _
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.babel import Babel
from flask_user import UserManager, SQLAlchemyAdapter
from flask_mail import Mail
import os


# create application
app = Flask(__name__)

#default app setting
settings_str = 'flaskapp.settings.ProductionConfig'
if os.environ.get('IS_DEV'):
    settings_str = 'flaskapp.settings.DevelopmentConfig'
app.config.from_object(settings_str)

#email
mail = Mail(app)

#babel
babel = Babel(app)
import babelhelper

#setup cache
cache = Cache(app)

#loggers
from flasklog import set_loggers
set_loggers()

# Database
db = SQLAlchemy(app)
import flaskapp.user.models
from flaskapp.user.models import User
import flaskapp.models


if app.config.get('IS_API', False):
    # from flaskapp.api_s import api_s_bp
    # app.register_blueprint(api_s_bp, url_prefix='/api')
    from flaskapp.api_s import urls
else:
    # Custom Exceptions error handler reg
    import flaskapp.app_exceptions
    import epages
    from flaskapp import psignals

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

    import flaskapp.urls
    from flaskapp.user import user_bp
    from flaskapp.store import store_bp
    from flaskapp.services_monitor import monitor_bp
    # BluePrints register here >>
    #app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(store_bp, url_prefix='/store')
    app.register_blueprint(monitor_bp, url_prefix='/monitor')

#flask-admin
#import adminhelper
