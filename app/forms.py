from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

from app.models import User

###########################################################
# 用户注册表单


class LoginForm(FlaskForm):
    ###########################################################
    # 表示我用于此表单的字段类型的四个类是直接从WTForms包导入的，
    # 因为Flask-WTF扩展不提供自定义版本。
    # 对于每个字段，将在类中将对象创建为类变量LoginForm。
    # 每个字段都有一个描述或标签作为第一个参数。
    # validators您在某些字段中看到的可选参数用于将验证行为附加到字段。
    # 该DataRequired验证程序只是简单地检查该字段不会提交空。
    # 还有更多的验证器，其中一些将以其他形式使用。
    ###########################################################

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

###########################################################
# 用户注册表单


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

###########################################################
# 用户个人信息编辑表单


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
