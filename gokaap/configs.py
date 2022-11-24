import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Flask Config"""
    SECRET_KEY = 'secretkey'
    SESSION_COOKIE_NAME = 'gokaap'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3307/gokaap?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION = 'list'

class DevelopmentConfig(Config):
    """Flask Config for dev"""
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFA = 1
    # front 호출 시 처리
    WTF_CSRF_ENAB = False

# pytest class
class TestingConfig(DevelopmentConfig):
    __test__ = False
    TESTIMG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "sqlite_test.db")}'

class ProducttionConfig(DevelopmentConfig):
    pass