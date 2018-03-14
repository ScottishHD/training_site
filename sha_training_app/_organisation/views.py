from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from ..models import Organisation
from . import organisation


@organisation.route('/')
def homepage():
    return render_template('organisation/index.html')
