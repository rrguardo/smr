# -*- coding: utf-8 -*-
"""
    flaskapp.user.models
    ~~~~~~~~~~~~~~
    
    SQLAlchemy user models.
"""


from flaskapp import db
import datetime
from flask_user import UserMixin
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

    # User Authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(100), nullable=False, default='')

    # User Email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    balance = db.Column(db.Float, default=0)
    auth_token = db.Column(db.String(120), unique=True)

    def is_active(self):
          return self.is_enabled

    def __repr__(self):
        return '<User %r>' % self.username

    def update_balance(self, amount):
        """Update the user balance + amount."""
        db.engine.execute("""UPDATE user
                    SET balance = balance+%s
                    WHERE id = %s
                    """ % (amount, self.id))

    def update_token(self):
        """ Use this function before save the model in database"""
        self.auth_token = uuid.uuid4().hex


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
