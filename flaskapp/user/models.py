# -*- coding: utf-8 -*-
"""
    flaskapp.user.models
    ~~~~~~~~~~~~~~
    
    SQLAlchemy user models.
"""


from flaskapp import db
import datetime
from flask.ext.login import UserMixin
import hashlib
import uuid


class Group(db.Model):
    """ User groups model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('User', backref='group', lazy='dynamic')
    
    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    """ System users model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    balance = db.Column(db.Float, default=0)
    auth_token = db.Column(db.String(120), unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.auth_token = uuid.uuid4().hex

    def __repr__(self):
        return '<User %r>' % self.username

    def update_password(self):
        """ Use this funct before save the model in database"""
        sh = hashlib.sha1()
        sh.update(self.password)
        self.password = sh.hexdigest()

    def update_token(self):
        """ Use this funct before save the model in database"""
        self.auth_token = uuid.uuid4().hex

    @property
    def is_active(self):
        """Returns True if this is an active user - in addition to being
        authenticated, they also have activated their account, not been
        suspended, or any condition your application has for rejecting an
        account. Inactive accounts may not log in (without being forced of
        course). """
        return True

    @property
    def is_authenticated(self):
        """ Returns True if the user is authenticated, i.e. they have
        provided valid credentials. (Only authenticated users will fulfill
        the criteria of login_required.)"""
        return True

    @property
    def is_anonymous(self):
        """ Returns True if this is an anonymous user. (Actual users should
        return False instead.)"""
        return False

    def get_id(self):
        """ Returns a unicode that uniquely identifies this user, and can be
        used to load the user from the user_loader callback. Note that this
        must be a unicode - if the ID is natively an int or some other type,
        you will need to convert it to unicode."""
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


def validate_user(username, password):
    """ Check user and password
        Returns a user object if validation success or None otherwise
    """
    try:
        sh = hashlib.sha1()
        sh.update(password)
        passw = sh.hexdigest()
        return User.query.filter_by(username=username, password=passw).first()
    except:
        from flaskapp import app
        import sys
        app.logger.error('ERROR validating user: %s' % sys.exc_info()[0])
    return None
