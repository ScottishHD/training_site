from flask_login import current_user
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup
from flask import current_app
from .simple_page import simple_page

def my_nav_bar():
    return Navbar(current_app.config.get('SITE_NAME'),
                  View('Home', 'simple_page.home'),
                  View('Blog', 'blogging.index'),
                  View('About', 'flat_pages.page', name='about'),
                  Subgroup(
                      'Apps',
                      View('Product A','flat_pages.page', name='producta'),
                      View('Product B','flat_pages.page', name='productb'),
                  ),
                 )

def sec_nav_bar():
    secnav = list(mynavbar().items)

    if current_user.is_authenticated:
        secnav.extend([
                View('Blog Editor', 'blogging.editor'),
                View('Profile', 'simple_page.profile'),
                ])

      if current_user.has_role('admin'):
            secnav.append(
                    View('Admin','admin.index')
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
    nav.register_element('admin_nav_bar', admin_nav_bar)
    nav.init_app(app)
