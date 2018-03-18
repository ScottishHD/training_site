import datetime
import json
import os

from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import admin
from .. import db, app
from ..forms import EditCourseForm, DeleteCourseForm, CreateCourseForm, OutcomeForm, ModuleForm
from ..models import User, Course, Module, Organisation, Outcome, Question, AnswerBank


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


@admin.route('/search_users')
def search_users():
    text = request.args['user']
    result = User.query.filter_by(username=text)

    return json.dumps({"results": result})


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


@admin.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
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


@admin.route('/edit_course/<course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    modules = Module.query.all()

    edit_form = EditCourseForm(obj=course)

    if edit_form.validate_on_submit():
        course.title = edit_form.title.data
        course.description = edit_form.description.data

        db.session.add(course)
        db.session.commit()

    return render_template('admin/edit_course.html', course=course, form=edit_form, modules=modules)


@admin.route('/delete_course/<course_id>', methods=['GET', 'POST'])
@login_required
def delete_course(course_id):
    delete_form = DeleteCourseForm()
    course = Course.query.filter_by(course_id=course_id)

    if delete_form.validate_on_submit():
        Course.query.filter_by(delete_form.title.data).delete()
        db.session.commit()

    return render_template('admin/delete_course.html', course=course, form=delete_course)


@admin.route('/view/<user_id>')
def view_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    courses = []
    organisation = None

    if user.account.organisation_id is not None:
        organisation = Organisation.query.filter_by(organisation_id=user.account.organisation_id).first()

    for enrolled in user.account.enrollments:
        course = Course.query.filter_by(course_id=enrolled.course_id).first()
        course.date_enrolled = user.account.enrollments
        course.modules_completed = enrolled.modules_completed
        courses.append(course)

        count = 0

    return render_template('admin/view_user.html', user=user, courses=courses, organisation=organisation)


@admin.route('/modules')
def modules():
    modules = Module.query.all()
    return render_template('admin/modules.html', modules=modules)


@admin.route('/create_module', methods=['GET', 'POST'])
def create_module():
    module_form = ModuleForm()

    if module_form.validate_on_submit():
        module = Module()
        module.title = module_form.module_title.data
        module.description = module_form.description.data

        questions = request.form['questions']
        answers = request.form['answers']
        fake_answers = request.form['fake_answers']
        fake_answers = fake_answers.split(',')

        # Save the module to the database first
        # this way we can reference the module
        # within the question object, and can
        # save it directly to the database with
        # direct relationship link
        db.session.add(module)
        db.session.commit()

        for i in range(0, len(fake_answers)):
            answer = AnswerBank()
            answer.answer = fake_answers[i]
            answer.module_id = module.module_id

            db.session.add(answer)
            db.session.commit()

        for i in range(0, len(questions)):
            question = Question()
            question.question = questions[i]
            question.answer = questions[i]
            question.module = module

            db.session.add(question)
            db.session.commit()

    return render_template('admin/create_module.html', form=module_form)


@admin.route('/edit_module/<module_id>', methods=['GET', 'POST'])
def edit_module(module_id):
    module = Module.query.filter_by(module_id=module_id).first()
    module_form = ModuleForm()

    if module_form.validate_on_submit():
        module.title = module_form.module_title.data
        module.description = module_form.description.data

    return render_template('admin/edit_module.html', module=module)


@admin.route('/delete_module/<module_id>')
def delete_module(module_id):
    module = Module.query.filter_by(module_id=module_id).first()
    return redirect(url_for('admin.modules'))


@admin.route('/outcomes')
def outcomes():
    outcomes = Outcome.query.all()
    return render_template('admin/outcomes.html', outcomes=outcomes)


@admin.route('/create_outcome', methods=['GET', 'POST'])
def create_outcome():
    outcome_form = OutcomeForm()

    if outcome_form.validate_on_submit():
        outcome = Outcome()
        if outcome_form.external_link:
            outcome.external = outcome_form.external_link.data
            outcome.resource_link = outcome_form.location.data
        else:
            outcome.resource_link = outcome_form.resource.data

        outcome.description = outcome_form.description.data

        db.session.add(outcome)
        db.session.commit()

    return render_template('admin/create_outcome.html', form=outcome_form)


@admin.route('/edit_outcome/<outcome_id>', methods=['GET', 'POST'])
def edit_outcome(outcome_id):
    outcome_form = OutcomeForm()
    outcome = Outcome.query.filter_by(outcome_id=outcome_id)

    if outcome_form.validate_on_submit():
        if outcome_form.external_link:
            outcome.resource_link = outcome_form.external_link.data
        else:
            outcome.resource_link = outcome_form.resource.data

        outcome.description = outcome_form.description.data

        db.session.add(outcome)
        db.session.commit()


@admin.route('/delete_outcome/<outcome_id>', methods=['GET', 'POST'])
def delete_outcome(outcome_id):
    outcome = Outcome.query.filter_by(outcome_id=outcome_id).first()

    return redirect(url_for('admin.outcomes'))
