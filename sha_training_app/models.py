import datetime

from flask_login import UserMixin
from sqlalchemy.orm import relationship
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

    modules = relationship(
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

    number_of_questions = db.Column(
        db.Integer
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.question_id')
    )

    questions = relationship(
        'Question',
        backref='questions',
        uselist=True
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

    modules_completed = relationship(
        'Module',
        backref='module',
        uselist=True
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    date_enrolled = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow()
    )

    date_completed = db.Column(
        db.DateTime,
        nullable=True
    )


class Question(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(
        db.Integer,
        primary_key=True
    )

    question = db.Column(
        db.String(64)
    )

    answer = db.Column(
        db.String(64)
    )


class AnswerBank(db.Model):
    answer_id = db.Column(
        db.Integer,
        primary_key=True
    )

    answer = db.Column(
        db.String(128)
    )

    module_id = db.Column(
        db.Integer,
        db.ForeignKey('modules.module_id')
    )
