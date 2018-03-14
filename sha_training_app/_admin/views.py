from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from ..forms import EditCourseForm, DeleteCourseForm
from ..models import User, Course
from . import admin
from .. import db


@admin.route('/')
@login_required
def homepage():
    user = User.query.filter_by(id=current_user.id).first()
    role = user.account.role.role_id

    if role == 2:
        return render_template('admin/index.html')
    else:
        return redirect(url_for('home.login'))


@admin.route('/users')
@login_required
def users():
    users = User.query.all()
    for user in users:

        user.date_joined = user.account.date_joined
        user.first_name = user.account.first_name
        user.last_name = user.account.last_name

    return render_template('admin/users.html', users=users)


@admin.route('/delete_user/<user_id>')
@login_required
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    return redirect(url_for('admin.users'))


@admin.route('/courses')
@login_required
def courses():
    courses = Course.query.all()
    for course in courses:
        user = User.query.filter_by(id=course.author).first()
        course.author_name = user.username
    return render_template('admin/courses.html', courses=courses)


@admin.route('/create_course')
@login_required
def create_course():
    return render_template('admin/create_course.html')


@admin.route('/edit_course/<course_id>')
@login_required
def edit_course(course_id):
    course = Course.query.filter_by(course_id=course_id)

    edit_form = EditCourseForm()

    if edit_form.validate_on_submit():
        course.title = edit_form.title.data
        course.description = edit_form.description.data
        # course.modules = course.modules
        course.image = edit_form.header_image.data

        db.session.add(course)
        db.session.commit()

    return render_template('admin/edit_course.html', course=course_id, form=edit_form)


@admin.route('/delete_course/<course_id>')
@login_required
def delete_course(course_id):
    delete_form = DeleteCourseForm()
    course = Course.query.filter_by(course_id=course_id)

    if delete_form.validate_on_submit():
        Course.query.filter_by(delete_form.title.data).delete()
        db.session.commit()

    return render_template('admin/delete_course.html', course=course, form=delete_course)
