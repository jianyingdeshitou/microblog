import os

basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['wsgi.url_scheme'] = 'https'

class Config(object):
    # 加密设置
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # 数据库设置
    DB_HOST = os.environ.get('DB_HOST')
    DB_ROOT_PASSWORD = os.environ.get('DB_ROOT_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:%s@%s:3306/%s' % \
        (DB_ROOT_PASSWORD, DB_HOST, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮件设置
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    # 分页
    POSTS_PER_PAGE = 3

