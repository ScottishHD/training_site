import datetime
import json
import os

from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import exists
from sqlalchemy.orm import Session

from . import admin
from .. import db, app, csrf
from ..forms import EditCourseForm, DeleteCourseForm, CreateCourseForm, OutcomeForm, ModuleForm
from ..models import User, Course, Module, Question, AnswerBank


@admin.route('/')
@login_required
def homepage():
    if current_user.account.has_role('admin'):
        user = User.query.filter_by(id=current_user.id).first()
        role = user.account.role.role_id

        if role == 2:
            return render_template('admin/index.html')
        else:
            return redirect(url_for('home.login'))
    else:
        return redirect('user.account')


@admin.route('/users')
@login_required
def users():
    if current_user.account.has_role('admin'):
        users = User.query.all()
        for user in users:
            user.date_joined = user.account.date_joined
            user.first_name = user.account.first_name
            user.last_name = user.account.last_name

        return render_template('admin/users.html', users=users)
    else:
        return redirect('user.account')


@admin.route('/search_users')
@login_required
def search_users():
    if current_user.account.has_role('admin'):
        text = request.args['user']
        result = User.query.filter_by(username=text)

        return json.dumps({"results": result})
    else:
        return redirect('user.account')


@admin.route('/delete_user/<user_id>')
@login_required
def delete_user(user_id):
    if current_user.account.has_role('admin'):
        User.query.filter_by(id=user_id).delete()
        return redirect(url_for('admin.users'))
    else:
        return redirect('user.account')


@admin.route('/courses')
@login_required
def courses():
    if current_user.account.has_role('admin'):
        courses = Course.query.all()
        for course in courses:
            user = User.query.filter_by(id=course.author).first()
            course.author_name = user.username
        return render_template('admin/courses.html', courses=courses)
    else:
        return redirect('user.account')


@admin.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    if current_user.account.has_role('admin'):
        course_form = CreateCourseForm()

        if course_form.validate_on_submit():
            course = Course()
            course.title = course_form.course_title.data
            course.description = course_form.description.data
            course.author = current_user.id
            course.modified = datetime.datetime.now()

            file = request.files['image']
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.root_path, 'static', 'uploads', 'images', filename))
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            course.image = filename

            db.session.add(course)
            db.session.commit()

        return render_template('admin/create_course.html', form=course_form)
    else:
        return redirect('user.account')


@admin.route('/edit_course/<course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    if current_user.account.has_role('admin'):
        course = Course.query.filter_by(course_id=course_id).first()
        modules = Module.query.all()

        edit_form = EditCourseForm(obj=course)

        if edit_form.validate_on_submit():
            course.title = edit_form.title.data
            course.description = edit_form.description.data
            modules

            db.session.add(course)
            db.session.commit()

        return render_template('admin/edit_course.html', course=course, form=edit_form, modules=modules)
    else:
        return redirect('user.account')


@admin.route('/delete_course/<course_id>', methods=['GET', 'POST'])
@login_required
def delete_course(course_id):
    if current_user.account.has_role('admin'):
        delete_form = DeleteCourseForm()
        course = Course.query.filter_by(course_id=course_id)

        if delete_form.validate_on_submit():
            Course.query.filter_by(delete_form.title.data).delete()
            db.session.commit()

        return render_template('admin/delete_course.html', course=course, form=delete_course)
    else:
        return redirect('user.account')


@admin.route('/view/<user_id>')
@login_required
def view_user(user_id):
    if current_user.account.has_role('admin'):
        user = User.query.filter_by(id=user_id).first()

        courses = []

        for enrolled in user.account.enrollments:
            course = Course.query.filter_by(course_id=enrolled.course_id).first()
            course.date_enrolled = user.account.enrollments
            course.modules_completed = enrolled.modules_completed
            courses.append(course)

        return render_template('admin/view_user.html', user=user, courses=courses)
    else:
        return redirect('user.account')


@admin.route('/modules')
def modules():
    if current_user.account.has_role('admin'):
        modules = Module.query.all()
        return render_template('admin/modules.html', modules=modules)
    else:
        return redirect('user.account')


@admin.route('/json_create_module', methods=['POST'])
def json_create_module():
    number_of_questions = request.form['number_of_questions']
    module = Module()
    module.number_of_questions = number_of_questions
    return json.dumps({'module': module})


@admin.route('/create_module', methods=['GET', 'POST'])
@login_required
def create_module():
    if current_user.account.has_role('admin'):
        module_form = ModuleForm()

        if module_form.validate_on_submit():
            module = Module()
            module.title = module_form.title.data
            module.description = module_form.description.data
            module.number_of_questions = module_form.number_of_questions.data

            db.session.add(module)
            db.session.commit()

            for question_iter in module_form.questions:
                question = Question()

                question.question = question_iter.question.data
                question.answer = question_iter.answer.data
                question.module = module

                db.session.add(question)
                db.session.commit()

            false_answers = module_form.false_answers.data.split(',')

            for false_answer_iter in false_answers:
                false_answer = AnswerBank()
                false_answer.answer = false_answer_iter
                false_answer.module = module

                db.session.add(false_answer)
                db.session.commit()

            return redirect(url_for('admin.modules'))

        return render_template('admin/create_module.html', form=module_form)
    else:
        return redirect('user.account')


@admin.route('/edit_module/<module_id>', methods=['GET', 'POST'])
@login_required
def edit_module(module_id):
    if current_user.account.has_role('admin'):
        module = Module.query.filter_by(module_id=module_id).first()
        module_form = ModuleForm(csrf_enabled=False)
        module_form.description.data = module.description
        questions = Question.query.filter_by(module=module).all()

        if module_form.validate_on_submit():
            module.title = module_form.title.data
            module.description = module_form.description.data
            module.number_of_questions = module_form.number_of_questions.data

            if module.number_of_questions != module_form.number_of_questions.data:

                for question_iter in module_form.questions:
                    exists = Session.query(exists().where(Question.question==question_iter.question.data))
                    if not exists:
                        question = Question()

                        question.question = question_iter.question.data
                        question.answer = question_iter.answer.data
                        question.module = module

                        db.session.add(question)
                        db.session.commit()

            db.session.add(module)
            db.session.commit()

        return render_template('admin/edit_module.html', module=module, form=module_form, questions=questions)
    else:
        return redirect('user.account')


@admin.route('/delete_module/<module_id>')
@login_required
def delete_module(module_id):
    if current_user.account.has_role('admin'):
        module = Module.query.filter_by(module_id=module_id).first()
        return redirect(url_for('admin.modules'))
    else:
        return redirect('user.account')
