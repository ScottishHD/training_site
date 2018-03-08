from flask import render_template
from . import home
from ..forms import LoginForm, RegisterForm
from .. import nav

nav.Bar('top',[
    nav.Item('Home', 'home.homepage'),
    nav.Item('Register', 'home.register'),
    nav.Item('Login', 'home.login')
])

@home.route('/')
def homepage():
    return render_template('home/index.html')


@home.route('/register')
def register():
    register_form = RegisterForm()

    return render_template('home/register.html', form=register_form)


@home.route('/login')
def login():
    login_form = LoginForm
    return render_template('home/login.html', form=login_form)