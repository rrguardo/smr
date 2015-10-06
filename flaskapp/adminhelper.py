# -*- coding: utf-8 -*-
"""
    flaskapp.adminhelper
    ~~~~~~~~~~~~~~~~~~~~

    Helper for flask-admin support.
"""
from flask.ext.login import current_user
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flaskapp import app, db
from flaskapp.user.models import User, Group


class MyModelView(ModelView):
    """ A ModelView with Authentication"""
    def is_accessible(self):
        """ Verifing that current user is authenticated"""
        return current_user.is_authenticated()

admin = Admin(app, base_template='admin/my_master.html')

# Add administrative views here
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Group, db.session))
