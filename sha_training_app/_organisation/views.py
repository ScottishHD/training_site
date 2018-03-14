from flask import render_template, url_for, redirect
from flask_login import current_user

from . import organisation
from ..models import Organisation


@organisation.route('/<org_id>')
def homepage(org_id):
    organisation = Organisation(organisation_id=org_id)
    if organisation.contact_id == current_user.id:
        return render_template('organisation/index.html')
    else:
        return redirect(url_for('user.homepage'))
