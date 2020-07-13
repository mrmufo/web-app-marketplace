import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bsrh.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = False  # os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = True  # os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ADMINS = ['buysellrenthire@gmail.com']
    ADS_PER_PAGE = 5
    LANGUAGES = ['en', 'es']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
