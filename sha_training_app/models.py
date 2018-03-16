from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

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

    account = relationship(
        'Account',
        backref='user',
        uselist=False
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

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    role = relationship(
        'Role',
        backref='role',
        uselist=False
    )

    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.role_id')
    )

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey('enrollments.enrol_id')
    )

    enrollments = relationship(
        'Enrollment',
        uselist=True,
    )

    organisation_id = db.Column(
        db.Integer,
        db.ForeignKey('organisation.organisation_id')
    )

    date_joined = db.Column(
        db.DateTime
    )

    first_name = db.Column(
        db.String(64)
    )

    last_name = db.Column(
        db.String(64)
    )

    def has_role(self, role_title):
        return self.role.title.lower() == role_title.lower()


class Organisation(db.Model):
    __tablename__ = 'organisation'

    organisation_id = db.Column(
        db.Integer,
        primary_key=True
    )

    display_name = db.Column(
        db.String(64)
    )

    contact = relationship(
        'User',
        backref='user',
        uselist=False
    )

    contact_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    size = db.Column(
        db.Integer,
        nullable=True
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

    author = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    module = relationship(
        'Module',
        backref='modules'
    )

    module_id = db.Column(
        db.Integer,
        db.ForeignKey('modules.module_id')
    )

    image = db.Column(
        db.String(256)
    )

    modified = db.Column(
        db.DateTime  # Not 100% sure about this
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

    outcome_id = db.Column(
        db.Integer,
        db.ForeignKey('outcomes.outcome_id')
    )

    outcomes = relationship(
        'Outcome',
        backref='modules'
    )


class Outcome(db.Model):
    __tablename__ = 'outcomes'

    outcome_id = db.Column(
        db.Integer,
        primary_key=True
    )

    resource_link = db.Column(
        db.String(128)
    )

    description = db.Column(
        db.String(256)
    )


class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    enrol_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.course_id')
    )

    module_id = db.Column(
        db.Integer,
        db.ForeignKey('modules.module_id')
    )

    outcome_id = db.Column(
        db.Integer,
        db.ForeignKey('outcomes.outcome_id')
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )



