import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

submission_download_dir = os.path.join(os.path.dirname(__file__), 'extractor', 'submissions')


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROJECT_ID = 'gluegun-app'

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    print('in', os.environ.get('DEV_DB_URI'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB_URI')
    DEBUG = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URI')
    TESTING = True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB_URI')
    DEBUG = False


config = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig,

    default=DevConfig
)
