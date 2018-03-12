from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(64),
        unique=True,
        index=True
    )

    email = db.Column(
        db.String(128),
        unique=True,
        index=True
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
        return User.query.get(int(self.id))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Account(db.Model):
    __tablename__ = 'accounts'

    account_index = db.Column(
        db.Integer,
        primary_key=True
    )

    fk_account_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    fk_account_role = db.Column(
        db.Integer,
        db.ForeignKey('roles.role_id')
    )

    courses = db.Column(
        db.String(64)
    )


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(64),
        unique=True
    )


class Course(db.Model):
    __tablename__ = 'courses'

    course_id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(64),
        unique=True
    )

    description = db.Column(
        db.String(256)
    )

    modules = db.Column(
        db.String(256)  # Array of integers {{module_id: 1},{module_id: 2},{module_id: 4},{module_id: 6}}
    )

    image = db.Column(
        db.String(256)
    )


class Module(db.Model):
    __tablename__ = 'modules'

    module_id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(64),
        unique=True
    )

    description = db.Column(
        db.String(256)
    )

    sets = db.Column(
        db.String(256)  # An array of integers relating to the ids of each of the sets
    )


class Set(db.Model):
    __tablename__ = 'sets'

    set_id = db.Column(
        db.Integer,
        primary_key=True
    )

    resource_link = db.Column(
        db.String(128)
    )

    description = db.Column(
        db.String(256)
    )

    quiz_link = db.Column(
        db.String(256)
    )
