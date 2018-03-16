from flask import render_template, redirect
from flask_login import login_required, current_user
from ..models import Course, Account, Role, User
from . import course


# The complete listing of courses that are on offer
@course.route('/listing')
def full_list():
    courses = Course.query.all()
    return render_template('course/list.html', courses=courses)


@course.route('/create', methods=['GET', 'POST'])
def create_course():
    if current_user.role.title != 'admin':
        return redirect('home.homepage')

    return render_template('course/create.html')


@course.route('/enrolled')
def enrolled():
    account = Account.query.filter_by(current_user.user_id)

    # TODO: Test this section ensure that it works
    for s in account.enrolled:
        # s = {'id':1, 'progress': 50}
        course = Course.query.filter_by(course_id=s['id'])

        course += {
            'is_complete': s['progress'] == 100
        }

        print(s)

    return """
    <h1>Temporary render</h1>
    """

@course.route('/<course_id>/<module_id>/<outcome_id>')
def continue_course(course_id, module_id, outcome_id):
    return render_template('course/outcome.html')