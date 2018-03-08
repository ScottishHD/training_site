import os
from utils import Utils, Config

def load_salt():
    if not os.path.isfile('slt'):
        salt = Utils.generate_salt(64)
        with open('slt', 'w') as salt_file:
            salt_file.write(salt)
    else:
        with open('slt', 'r') as salt_file:
            salt = salt_file.read()
    return salt



class Config(object):
    """
    Common configuration options
    """
    config = Config()
    config.load_config()

    SQLALCHEMY_DATABASE_DRIVER = config.get('database_driver', 'mysql+pymysql')
    SQLALCHEMY_DATABASE_USERNAME = config.get('database_username', 'root')
    SQLALCHEMY_DATABASE_PASSWORD = config.get('database_password', 'root')
    SQLALCHEMY_DATABASE_HOST = config.get('database_host', 'localhost')
    SQLALCHEMY_DATABASE_NAME = config.get('database_name', 'sha_training')
    SQLALCHEMY_DATABASE_PORT = config.get('database_port', 3306)
    SQLALCHEMY_DATABASE_URI = '{}//{}:{}@{}:{}/{}'.format(SQLALCHEMY_DATABASE_DRIVER, SQLALCHEMY_DATABASE_USERNAME, SQLALCHEMY_DATABASE_PASSWORD, SQLALCHEMY_DATABASE_HOST, SQLALCHEMY_DATABASE_PORT, SQLALCHEMY_DATABASE_NAME)

    SECURITY_PASSWORD_SALT = load_salt()
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER = config.get('uploads_folder_name', 'uploads')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATION = True
    SQLALCHEMY_DEBUG = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_DEBUG = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
