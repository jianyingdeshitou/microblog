from flask import render_template, flash, redirect, url_for
from flask import request

from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required

from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.models import User

###############################################################################
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)


###############################################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果当前用户已经登录
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # 验证用户登录
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        # 1. 如果登录URL没有next参数，则将用户重定向到索引页面。
        # 2. 如果登录URL包含next设置为包含域名的完整URL 的参数，则会将用户重定向到索引页。
        # 攻击者可以在next参数中向恶意站点插入URL ，
        # 因此应用程序仅在URL为相对时重定向，
        # 这可确保重定向与应用程序保持在同一站点内。
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # 3. 如果登录URL包含next设置为相对路径的参数（或者换句话说，没有域部分的URL），
        # 则将用户重定向到该URL。
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

###############################################################################

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))