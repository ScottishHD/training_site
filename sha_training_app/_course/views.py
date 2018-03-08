from flask import render_template
from flask_login import login_required, current_user
from ..models import Course, Account, User
from . import course

@course.route('/listing')
def full_list():
    courses = Course.query.all()