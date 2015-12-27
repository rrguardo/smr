# -*- coding: utf-8 -*-
"""
    flaskapp.admin.views
    ~~~~~~~~~~~~~~~~~~~~

    User forms here.
"""

from flask_wtf import Form, RecaptchaField
from wtforms import BooleanField, TextField, PasswordField, validators, \
                    ValidationError
from flaskapp.user.models import User, validate_user
from flask.ext.login import login_user, current_user
from gettext import gettext as _


class RegistrationForm(Form):
    username = TextField(_(u'Username'), [validators.Length(min=4, max=25)])
    email = TextField(_(u'Email Address'), [validators.Length(min=6, max=35),
                                        validators.Email()])
    password = PasswordField(_(u'New Password'), [validators.Required(),
                validators.EqualTo('confirm', 
                                   message=_(u'Passwords must match')),
                validators.Length(min=6, max=35)])
    confirm = PasswordField(_(u'Repeat Password'))
    accept_tos = BooleanField(_(u'I accept the TOS'), 
                              [validators.Required()])
    recaptcha = RecaptchaField()

    def validate_email(form, field):
        """ validate email"""
        try:
            cnt = User.query.filter_by(email=form.email.data).count()
            if cnt > 0:
                raise ValidationError(_(u"Select a different email."))
        except:
            raise ValidationError(_(u"Select a different email."))

    def validate_username(form, field):
        """ validate user name"""
        try:
            cnt = User.query.filter_by(username=form.username.data).count()
            if cnt > 0:
                raise ValidationError(_(u"Select a different username."))
        except:
            raise ValidationError(_(u"Select a different username."))


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


class PasswChangeForm(Form):
    old_password = PasswordField(_(u'Old Password'), [validators.Required()])
    new_password = PasswordField(_(u'New Password'), [validators.Required(),
        validators.Length(min=6, max=35)])
    confirm_password = PasswordField(_(u'Confirm Password'),
        [validators.Required()])

    def validate_confirm_password(form, field):
        """Validate password confirmation."""
        conf = field.data
        npw = form['new_password'].data
        if conf != npw:
            raise ValidationError(
                _(u"New password and confirmation don't match."))

    def validate_old_password(form, field):
        """ Validation will check old password"""
        passw = field.data
        user = current_user.username
        log_user = validate_user(user, passw)
        if log_user is None:
            raise ValidationError(_(u"Incorrect password."))
