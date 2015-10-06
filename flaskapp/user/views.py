# -*- coding: utf-8 -*-
"""
    flaskapp.user.views
    ~~~~~~~~~~~~~~~~~~~~

    User views here.
"""


from flask import request, g, redirect, url_for, render_template, flash
from flask.views import View
from flaskapp.user.forms import RegistrationForm, LoginForm
from flask.ext.login import login_required, logout_user
from gettext import gettext as _


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

@login_required
def panel():
    """ User panel view"""
    return render_template('user/panel.html')

@login_required
def logout():
    logout_user()
    return redirect(request.args.get("next") or '/')

