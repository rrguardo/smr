
from flask_wtf import Form, RecaptchaField
from wtforms import BooleanField, TextField, PasswordField, validators, ValidationError, TextAreaField
from gettext import gettext as _


class ContactForm(Form):
    subject = TextField(_(u'Subject'), [validators.Length(min=2, max=80)])
    message = TextAreaField(_(u'Message'), [validators.Length(min=10, max=500)])
    recaptcha = RecaptchaField()
