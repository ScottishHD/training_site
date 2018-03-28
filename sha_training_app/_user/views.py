from flask import render_template, url_for, redirect, send_file
from flask_login import login_required, current_user
from mailmerge import MailMerge
from datetime import date
from ..models import User, Course, Enrollment, Module, Question, AnswerBank
from . import user
import random


@user.route('/account')
@login_required
def account():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    courses = []
    completed_courses = []

    for enrollment in enrollments:
        course = Course.query.filter_by(course_id=enrollment.course_id).first()
        if enrollment.completed:
            completed_courses.append(course)
        else:
            enrollment.course = course
            courses.append(course)

    return render_template('user/account.html', courses=courses, completed_courses=completed_courses)


@user.route('/enrol/<course_id>', methods=['GET', 'POST'])
@login_required
def enrol(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    enrollment = Enrollment(
        course_id=course_id,
        user_id=current_user.id
    )
    current_user.account.enrollments.append(enrollment)
    return redirect(url_for('home.homepage'))


@user.route('/download/<course_id>')
@login_required
def certificate(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    template = url_for('static', filename='uploads/documents/Certificate Base.docx')

    name = '{} {}'.format(current_user.account.first_name, current_user.account.last_name)
    date_obj = '{:%d-%b-%Y}'.format(date.today()),

    document = MailMerge(template)
    document.merge(
        Name=name,
        Course=course.title,
        Date=date_obj
    )

    new_name = '{} - {}.docx'.format(name, date_obj)

    document.write(new_name)

    return send_file(url_for('static', filename='uploads/documents/new_name'))


@user.route('/enrolled')
def course_listing():
    enrollments = current_user.account.enrollments
    courses = []
    for enrollment in enrollments:
        course = Course.query.filter_by(course_id=enrollment.course_id).first()
        courses.append(course)
    return render_template('user/courses.html', courses=courses)


@user.route('/view_course/<course_id>')
@login_required
def view_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    return render_template('user/view_course.html', course=course)


@user.route('/<course_id>/<module_id>')
def resume_course(course_id, module_id):
    module = Module.query.filter_by(module_id=module_id)
    questions = Question.query.filter_by(module_id=module_id)
    false_answers = AnswerBank.query.filter_by(module_id=module_id).all()

    for question in questions:
        question.answers = []
        question.answers.append(question.answer)
        for i in range(0, 4):
            question.answers.append(false_answers[random.randint(0, len(false_answers))])

        random.shuffle(question.answers)

    return render_template('user/module.html', module=module, questions=questions)
