from datetime import datetime

from flask import render_template, flash, redirect, url_for
from flask import request

from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required

from werkzeug.urls import url_parse

from app import app
from app import db

from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.forms import PostForm

from app.models import User
from app.models import Post


###############################################################################
# 首页
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))

    posts = current_user.followed_posts().all()
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts)


###############################################################################
# 用户登录页
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

###############################################################################
# 用户注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

###############################################################################
# 用户个人资料页面
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


###############################################################################
# 获取上次访问时间
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

###############################################################################
# 用户个人信息编辑页面
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

#######################################################################
# 关注
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

#######################################################################
# 取消关注
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

#######################################################################
# 探索页面
@app.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)

