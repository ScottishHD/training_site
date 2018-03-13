from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import User, Account, Role, Course
from . import admin

@admin.route('/')
@login_required
def homepage():
    account = Account.query.filter_by(fk_account_id=current_user.id).first()
    if account.fk_account_role == 1:
        return render_template('admin/index.html')
    else:
        return redirect(url_for('user.login'))


@admin.route('/users')
@login_required
def users():
    users = User.query.all()
    template_users = []
    for user in users:
        account = Account.query.filter_by(fk_account_id=user.id).first()

        user.date_joined = account.date_joined
        user.first_name = account.first_name
        user.last_name = account.last_name

        # template_users += user

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

    course_form = EditCourseForm()

    if form.validate_on_submit():
        course.title = course_form.title.data
        course.description = course_form.description.data
        # course.modules = course.modules
        course.image = course_form.header_image.data

        db.session.add(course)
        db.session.commit()

    return render_template('admin/edit_course.html', course=course_id, form=course_form)

@admin.route('/delete_course/<course_id>')
@login_required
def delete_course(course_id):
    delete_form = DeleteCourseForm()

    if form.validate_on_submit():
        Course.query.filter_by(delete_form.title.data).delete()
        db.session.commit()

    return render_template('admin/delete_course.html', course=course, form=delete_course)
