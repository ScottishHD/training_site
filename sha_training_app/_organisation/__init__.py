from flask import Blueprint

organisation = Blueprint('organisation', __name__)

from . import views
