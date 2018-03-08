from flask import render_template, redirect, url_for
from flask_login import login_user
from . import home
from ..models import  User
from ..forms import LoginForm, RegisterForm
from .. import nav

# Need to make this dynamic somehow
nav.Bar('top', [
    nav.Item('Home', 'home.homepage'),
    nav.Item('Register', 'home.register'),
    nav.Item('Login', 'home.login')
])

@home.route('/')
def homepage():
    return render_template('home/index.html')


@home.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    # The user has submitted the form, let's make sure it's valid
    if register_form.validate_on_submit():
        # Create a new user from the form data
        user = User(
            username=register_form.username.data,
            email = register_form.email.data,
            password = register_form.password.data
        )

        # At this point the user has been registered and should
        # have been sent a confirmation email
        return render_template('home/registration_success.html')
    # Show the user the registration form
    return render_template('home/register.html', form=register_form)


@home.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user)
            redirect(url_for('user.account'))

    return render_template('home/login.html', form=login_form)
