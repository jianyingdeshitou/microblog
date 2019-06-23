from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

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



