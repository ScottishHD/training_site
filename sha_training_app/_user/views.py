from flask import render_template
from flask_login import login_required, current_user
from . import user
from .. import nav

nav.Bar('top', [
    nav.Item('Home', 'home.homepage'),
    nav.Item('Account', 'user.homepage'),
    nav.Item('Courses', 'course.full_list')
])

@user.route('/')
@login_required
def homepage():
    return render_template('user/index.html')
