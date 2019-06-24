import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler

import os

from flask import Flask

# 小写的“config”是Python模块config.py的名称，
# 显然具有大写“C”的那个是实际的类。
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

from flask_mail import Mail

from flask_bootstrap import Bootstrap

#################################################
# 反向代理设置
class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

# app
app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = ReverseProxied(app.wsgi_app)

# 数据库
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 登录
login = LoginManager(app)
login.login_view = 'login'


# 电子邮件支持
mail = Mail(app)

# bootstrap 模版
bootstrap = Bootstrap(app)

# 通过电子邮件记录错误
# 命令行测试：python -m smtpd -n -c DebuggingServer localhost:8025
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

# 通过日志记录错误
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                    backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Microblog startup')

from app import routes, models, errors