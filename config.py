import os

basedir = os.path.abspath(os.path.dirname(__file__))


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
submission_download_dir = os.path.join(os.path.dirname(__file__), 'extractor', 'submissions')


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB_URI')
    DEBUG = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URI')
    TESTING = True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DB_URI')
    DEBUG = False


config = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig,

    default=DevConfig
)
