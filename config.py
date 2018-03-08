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

    SQLALCHEMY_DATABASE_DRIVER = config.get('mysql+pymysql', 'database_driver')
    SQLALCHEMY_DATABASE_USERNAME = config.get('root', 'database_username')
    SQLALCHEMY_DATABASE_PASSWORD = config.get('root', 'database_password')
    SQLALCHEMY_DATABASE_HOST = config.get('localhost', 'database_host')
    SQLALCHEMY_DATABASE_NAME = config.get('sha_training', 'database_name')
    SQLALCHEMY_DATABASE_PORT = config.get(3306, 'database_port')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql//root:root@localhost/sha_training'
    # SQLALCHEMY_DATABASE_URI = '{}//{}:{}@{}:{}/{}'.format(SQLALCHEMY_DATABASE_DRIVER, SQLALCHEMY_DATABASE_USERNAME, SQLALCHEMY_DATABASE_PASSWORD, SQLALCHEMY_DATABASE_HOST, SQLALCHEMY_DATABASE_PORT, SQLALCHEMY_DATABASE_NAME)

    SECURITY_PASSWORD_SALT = load_salt()
    SECRET_KEY = Utils.generate_salt(64)
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
