import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nie-zgadniesz-XD'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465) or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true') == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'spataj1234@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'koty1253')
    ADMINS = ['spataj1234@gmail.com']
    POSTS_PER_PAGE = 25