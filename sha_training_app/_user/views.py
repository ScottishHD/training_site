from flask import render_template
from flask_login import login_required, current_user
from ..models import User
from . import user


@user.route('/')
@login_required
def homepage():
    return render_template('user/index.html')

@user.route('/account/<user_id>')
@login_required
def account(user_id):
    user = User.query.filter_by(id=user_id)
    return render_template('user/index.html', user=user)
