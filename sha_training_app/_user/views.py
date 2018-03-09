from flask import render_template
from flask_login import login_required
from . import user


@user.route('/')
@login_required
def homepage():
    return render_template('user/index.html')
