# -*- coding: utf-8 -*-
"""
    flaskapp.admin.views
    ~~~~~~~~~~~~~~~~~~~~

    User forms here.
"""

from flask_wtf import Form, RecaptchaField
from wtforms import BooleanField, TextField, PasswordField, validators, \
                    ValidationError
from flaskapp import db
from flaskapp.user.models import User, validate_user
from flask.ext.login import login_user
from gettext import gettext as _


class RegistrationForm(Form):
    username = TextField(_(u'Username'), [validators.Length(min=4, max=25)])
    email = TextField(_(u'Email Address'), [validators.Length(min=6, max=35),
                                        validators.Email()])
    password = PasswordField(_(u'New Password'), [validators.Required(),
                validators.EqualTo('confirm', 
                                   message=_(u'Passwords must match'))])
    confirm = PasswordField(_(u'Repeat Password'))
    accept_tos = BooleanField(_(u'I accept the TOS'), 
                              [validators.Required()])
    recaptcha = RecaptchaField()
    
    def validate_username(form, field):
        """ This will also save the new user"""
        try:
            #ensuring other fields are valid before save to DB
            if form.email.validate(form) and form.password.validate(form) and \
            form.accept_tos.validate(form) and form.recaptcha.validate(form):
                user = User(form.username.data, form.email.data, 
                            form.password.data)
                #storing passw hash
                user.update_password()
                db.session.add(user)
                db.session.commit()
        except:
            raise ValidationError(_(u"Please select a different username \
                                    or try with other email."))


class LoginForm(Form):
    username = TextField(_(u'Username'), [validators.Required()])
    password = PasswordField(_(u'Password'), [validators.Required()])
    
    def validate_password(form, field):
        """ Validation will also login the user"""
        user = form['username'].data
        passw = field.data
        log_user = validate_user(user, passw)
        print "Logged User: ", log_user
        if log_user is None:
            raise ValidationError(_(u"Incorrect username or password."))
        else:
            login_user(log_user)

