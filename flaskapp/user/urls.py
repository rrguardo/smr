# -*- coding: utf-8 -*-
"""
    flaskapp.user.urls
    ~~~~~~~~~~~~~~~~~~~
    
    Add all url <-> view maps here for user sub-package.
"""


from flaskapp.user import user_bp
from flaskapp.user.views import *


user_bp.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
user_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
user_bp.add_url_rule('/logout/', 'logout', logout)
user_bp.add_url_rule('/panel/', 'panel', panel)
user_bp.add_url_rule('/stats/', 'stats', stats)
user_bp.add_url_rule('/add_credits/', 'add_credits', add_credits)

user_bp.add_url_rule('/new_token/',
    view_func=TokenView.as_view('get_new_auth_token'))

user_bp.add_url_rule('/upd_pw/',
    view_func=ChangePasswView.as_view('upd_pw'))
