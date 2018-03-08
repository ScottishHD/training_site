from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page!'
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app, db)

    from _home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from _admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from _user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app