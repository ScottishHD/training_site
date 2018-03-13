from flask import render_template
from flask_login import login_required, current_user
from ..models import User
from . import user


@user.route('/')
@login_required
def homepage():
    return render_template('user/index.html')

@user.route('/account')
@login_required
def account():
    return render_template('user/index.html')


@user.route('/enrol/<course_id>', methods=['GET', 'POST'])
@login_required
def enrol(course_id):
    return redirect(url_for('home.homepage'))


@user.route('/enrolled')
def course_listing():
    courses = None
    return render_template('user/courses.html', courses=courses)
