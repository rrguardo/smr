# -*- coding: utf-8 -*-
"""
    flaskapp.user.views
    ~~~~~~~~~~~~~~~~~~~~

    User views here.
"""


from flask import request, g, redirect, url_for, render_template,\
    flash, jsonify
from flask.views import View
from flask_wtf import Form
from flaskapp.user.forms import RegistrationForm, LoginForm, PasswChangeForm
from flask.ext.login import login_required, logout_user, current_user
from gettext import gettext as _
import datetime
from flaskapp import db
from flaskapp.models import SMS_Status
from flaskapp.user.models import User
from sqlalchemy import and_


class FormView(View):
    """ Abstract view with form pattern"""
    methods = ['GET', 'POST']

    def get_form_class(self):
        """ returns the form class to use"""
        raise NotImplementedError()

    def get_template(self):
        """ template to use"""
        raise NotImplementedError()

    def post_inst(self, form, request):
        """ Instrucctions to execute if request.method == 'POST' """
        raise NotImplementedError()

    def dispatch_request(self):
        formclass = self.get_form_class()
        form = formclass(request.form)
        if request.method == 'POST' and form.validate():
            return self.post_inst(form, request)
        return render_template(self.get_template(), form=form)


class RegisterView(FormView):
    """ Reg new user view"""

    def get_form_class(self):
        return RegistrationForm

    def get_template(self):
        return 'user/register.html'

    def post_inst(self, form, request):
        user = User(form.username.data, form.email.data,
            form.password.data)
        # storing passw hash
        user.update_password()
        db.session.add(user)
        db.session.commit()
        flash(_(u'Thanks for registering'))
        return redirect(url_for('user.login'))


class LoginView(FormView):
    """ Login user view"""
    
    def get_form_class(self):
        return LoginForm
    
    def get_template(self):
        return 'user/login.html'
    
    def post_inst(self, form, request):
        flash(_(u"Logged in successfully."))
        return redirect(request.args.get("next") or url_for("user.panel"))


class ChangePasswView(FormView):
    """ ChangePassw user view"""

    def get_form_class(self):
        return PasswChangeForm

    def get_template(self):
        return 'user/update_password.html'

    def post_inst(self, form, request):
        current_user.password = form["new_password"].data
        current_user.update_password()
        db.session.commit()
        flash(_(u"Password changed successfully."))
        return redirect(request.args.get("next") or url_for("user.panel"))


class TokenView(FormView):
    """ Toke user view"""

    def get_form_class(self):
        return Form

    def get_template(self):
        return 'user/panel.html'

    def post_inst(self, form, request):
        current_user.update_token()
        db.session.commit()
        flash(_(u'Auth token updated'))
        return redirect(request.args.get("next") or url_for("user.panel"))


@login_required
def panel():
    """ User panel view"""
    return render_template('user/panel.html', form=Form())


@login_required
def logout():
    logout_user()
    return redirect(request.args.get("next") or '/')


@login_required
def stats():
    """ User stats view"""
    current_time = datetime.datetime.now()
    current_time = current_time - datetime.timedelta(weeks=2)
    result = SMS_Status.query.filter(and_(SMS_Status.user_id == current_user.id,
        SMS_Status.send_date > current_time)
        ).order_by(SMS_Status.id.desc()).limit(1000)
    return render_template('user/stats.html', data=result)


@login_required
def add_credits():
    """ Buy credits panel view"""
    return render_template('user/add_credits.html')
