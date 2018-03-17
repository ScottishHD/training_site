from flask import current_app
from flask_login import current_user
from flask_nav import Nav
from flask_nav.elements import Navbar, View


def my_nav_bar():
    return Navbar(
        current_app.config.get('SITE_NAME'),
        View('Home', 'home.homepage'),
    )


def unauthenticated_nav():
    nav = list(my_nav_bar().items)

    nav.extend([
        View('Login', 'home.login'),
        View('Register', 'home.register')
    ])
    return Navbar(current_app.config.get('SITE_NAME'), *nav)


def sec_nav_bar():
    secnav = list(my_nav_bar().items)

    if current_user.is_authenticated and not current_user.account.has_role('admin'):
        secnav.extend([
            View('Account', 'user.account'),
            View('Courses', 'user.course_listing'),
            View('Log out', 'home.logout')
        ])

    if current_user.account.has_role('admin'):
        secnav.extend([
            View('Account', 'user.account'),
            View('Admin', 'admin.homepage'),
            View('Users', 'admin.users'),
            View('Courses', 'admin.courses'),
            View('Modules', 'admin.modules'),
            View('Outcomes', 'admin.outcomes'),
            View('Log out', 'home.logout')
        ])
    else:
        secnav.extend([
            View('Log in', 'home.login')
        ])
    return Navbar(current_app.config.get('SITE_NAME'), *secnav)


def configure_nav(app):
    nav = Nav()
    nav.register_element('my_nav_bar', my_nav_bar)
    nav.register_element('sec_nav_bar', sec_nav_bar)
    nav.register_element('unauthenticated_nav', unauthenticated_nav)
    nav.init_app(app)
