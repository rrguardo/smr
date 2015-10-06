# -*- coding: utf-8 -*-
"""
    Lettuce steps definition.
"""

import sys
from lettuce import *
from selenium import webdriver
import lettuce_webdriver.webdriver
sys.path.append('../')   # making  'flaskapp' package accessible
sys.path.append('../../')   # making  'runserver' module accessible
from flaskapp.user.models import User
from flaskapp import db


def def_database():
    """ Prepare database for lettuce tests"""
    try:
        #removing users to signup tests
        qr = db.session.query(User).filter_by(username='admin')
        qr.delete()
        qr1 = db.session.query(User).filter_by(username='guest')
        qr1.delete()
        db.session.commit()
    except:
        pass

@before.all
def setup_browser():
    world.browser = webdriver.PhantomJS()
    def_database()

@after.all
def close_browser(total):
    world.browser.quit()

