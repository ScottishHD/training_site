from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from ..models import User, Course, Enrollment
from . import user


@user.route('/account')
@login_required
def account():
    return render_template('user/index.html')


@user.route('/enrol/<course_id>', methods=['GET', 'POST'])
@login_required
def enrol(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    enrollment = Enrollment(
        course_id= course_id,
        user_id=current_user.id
    )
    current_user.account.enrollments.append(enrollment)
    return redirect(url_for('home.homepage'))


@user.route('/enrolled')
def course_listing():
    enrollments = current_user.account.enrollments
    courses = []
    for enrollment in enrollments:
        course = Course.query.filter_by(course_id=enrollment.course_id).first()
        courses.append(course)
    return render_template('user/courses.html', courses=courses)
