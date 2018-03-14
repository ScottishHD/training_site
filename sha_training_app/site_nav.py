from flask_login import current_user
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup
from flask import current_app


def my_nav_bar():
    return Navbar(
        current_app.config.get('SITE_NAME'),
        View('Home', 'home.homepage'),
    )


def unauthenticated_nav():
    nav = list(my_nav_bar().items)

    if not current_user.is_authenticated:
        nav.extend([
            View('Login', 'home.login'),
            View('Register', 'home.register')
        ])


def sec_nav_bar():
    secnav = list(my_nav_bar().items)

    if current_user.is_authenticated:
        secnav.extend([
            View('Account', 'blogging.editor'),
            View('Profile', 'simple_page.profile'),
        ])

    if current_user.has_role('admin'):
        secnav.append(
            View('Admin', 'admin.index')
        )
        secnav.append(View('Log out', 'security.logout'))
    else:
        secnav.append(
            View('Log in', 'security.login')
        )
    return Navbar(current_app.config.get('SITE_NAME'), *secnav)


def configure_nav(app):
    nav = Nav()
    nav.register_element('my_nav_bar', my_nav_bar)
    nav.register_element('sec_nav_bar', sec_nav_bar)
    # nav.register_element('admin_nav_bar', admin_nav_bar)
    nav.init_app(app)
