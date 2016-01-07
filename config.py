import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = 'mysql://root:{mysqlpassword}@{mysqlurl}:{mysqlport}/{database}'.format(mysqlpassword=os.environ.get('MYSQL_ENV_MYSQL_ROOT_PASSWORD'), mysqlurl=os.environ.get('MYSQL_PORT_3306_TCP_ADDR'), mysqlport=os.environ.get('MYSQL_PORT_3306_TCP_PORT'), database=os.environ.get('MYSQL_ENV_MYSQL_DATABASE'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

config = {
    'development': DevelopmentConfig,
    }
