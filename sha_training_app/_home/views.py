from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from . import home
from ..models import User, Account, Role, Course
from ..forms import LoginForm, RegisterForm
from sha_training_app import db


@home.route('/')
def homepage():
    courses = Course.query.limit(5)
    return render_template('home/index.html', courses=courses)


@home.route('/courses')
def course_listing():
    courses = Course.query.all()
    return render_template('home/courses.html', courses=courses, standalone=True)


@home.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    # The user has submitted the form, let's make sure it's valid
    if register_form.validate_on_submit():
        # Create a new user from the form data
        user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            password=register_form.password.data
        )

        role = Role.query.filter_by(role_id=1).first()

        account = Account(
            role_id=role.role_id
        )

        user.account.append(account)

        db.session.add(user)
        db.session.add(account)
        db.session.commit()

        # At this point the user has been registered and should
        # have been sent a confirmation email
        return render_template('home/registration_success.html')
    # Show the user the registration form
    return render_template('home/register.html', form=register_form)


@home.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        print(user.verify_password(login_form.password.data))
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user)
            return redirect(url_for('user.account'))

    return render_template('home/login.html', form=login_form)


@home.route('/logout')
def logout():
    logout_user()  # This should kill the session
    return redirect(url_for('home.homepage'))
