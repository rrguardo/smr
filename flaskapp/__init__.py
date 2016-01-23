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
from flask.ext.login import LoginManager
from flask_mail import Mail


# create application
app = Flask(__name__)
#default app setting
app.config.from_object('flaskapp.settings.TestingConfig')

#email
mail = Mail(app)

#babel
babel = Babel(app)
import babelhelper

#setup cache
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

#loggers
from flasklog import set_loggers
set_loggers()

# Database
db = SQLAlchemy(app)
import flaskapp.user.models
from flaskapp.user.models import User
import flaskapp.models

# Custom Exceptions errorhandler reg
import flaskapp.app_exceptions
import epages

#Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"
login_manager.login_message = _(u"Please log in to access this page.")

@login_manager.user_loader
def load_user(userid):
    try:
        return User.query.get(userid)
    except:
        return None

# Views import here >>
import flaskapp.urls #lazy-optimized views load
#import flaskapp.views
#from flaskapp.api import api_bp
from flaskapp.api_s import api_s_bp
from flaskapp.user import user_bp
from flaskapp.store import store_bp
# BluePrints register here >>
#app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(api_s_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(store_bp, url_prefix='/store')


#flask-admin
#import adminhelper
