from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from run import db, login_manager
from utils import Utils

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(64),
        unique = True,
        index = True
    )

    email = db.Column(
        db.String(128),
        unique = True,
        index = True
    )

    password_hash = db.Column(
        db.String(128)
    )

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return User.query.get(int(self.user_id))

class Account(db.Model):
    __tablename__ = 'account'

    account_index = db.Column(
        db.Integer,
        primary_key=True
    )

    account_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id')
    )
