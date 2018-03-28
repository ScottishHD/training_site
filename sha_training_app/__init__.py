from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import app_config
from .site_nav import configure_nav

app = Flask(__name__, instance_relative_config=True)

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect(app)


def create_app(config_name):
    configure_nav(app)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page!'
    login_manager.login_view = 'home.login'

    migrate = Migrate(app, db)
    from . import models

    from sha_training_app._home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from sha_training_app._admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from sha_training_app._user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    return app
