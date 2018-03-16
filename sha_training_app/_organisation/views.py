from flask import render_template, url_for, redirect
from flask_login import current_user
from . import organisation
from ..models import Organisation, User, Account
from ..forms import OrganisationRegisterForm
from .. import db


@organisation.route('/<org_id>')
def homepage(org_id):
    organisation = Organisation(organisation_id=org_id)
    if organisation.contact_id == current_user.id:
        return render_template('organisation/index.html')
    else:
        return redirect(url_for('user.homepage'))


@organisation.route('/register')
def register():
    register_form = OrganisationRegisterForm()

    if register_form.validate_on_submit():
        user = User.query.filter_by(contact_email=register_form.contact_email.data).first()
        organisation = Organisation()
        if user is not None:
            organisation.contact = user
        else:
            # Do we want to force it that the staff member should be registered to be
            # a contact for an organisation
            pass

        organisation.display_name = register_form.organisation_name.data
        organisation.size = register_form.size.data

        db.session.add(organisation)
        db.session.commit()

        return redirect(url_for('organisation.homepage', org_id=organisation.organisation_id))

    return render_template('organisation/register.html')

@organisation.route('/<org_id>/staff')
def staff_listing(org_id):
    organisation = Organisation.query.filter_by(organisation_id=org_id)
    if organisation.contact == current_user:
        staff = Account.query.filter_by(organisation)
        return render_template('organisation/staff.html')
    else:
        return redirect(url_for('user.homepage'))