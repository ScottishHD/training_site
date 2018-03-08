from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import app_config

app = Flask(__name__, instance_relative_config=True, debug=True)
db = SQLAlchemy()
login_manager - LoginManager()

def create_app(config_name):
    global db
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page!'
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app, db)
    from . import models