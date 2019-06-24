from datetime import datetime

from hashlib import md5

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from app import db
from app import login

#######################################################################
# 用户数据库模型


class User(UserMixin, db.Model):
    # 用户id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    username = db.Column(db.String(64), index=True, unique=True)
    # 邮箱
    email = db.Column(db.String(120), index=True, unique=True)
    # 密码哈希值
    password_hash = db.Column(db.String(128))
    # 个人简介
    about_me = db.Column(db.String(140))
    # 最后访问时间
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 头像
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

#######################################################################


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#######################################################################
# 文章

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

#######################################################################
