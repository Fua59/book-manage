import wtforms
from wtforms.fields.simple import PasswordField
from wtforms.validators import Length, EqualTo

# 注册表单验证器
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=12, max=12, message="用户名只能为12位！")])
    password = wtforms.PasswordField(validators=[Length(min=5, max=20, message="密码只能为5-20位！")])
    password_confirm = wtforms.PasswordField(validators=[EqualTo("password", message="密码不一致！")])

# 登录
class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=5, max=12, message="用户名只能为12位！")])
    password = wtforms.PasswordField(validators=[Length(min=5, max=20, message="密码只能为5-20位！")])

class PasswordForm(wtforms.Form):
    password = wtforms.PasswordField(validators=[Length(min=5, max=20, message="密码只能为5-20位！")])
    password_confirm = wtforms.PasswordField(validators=[EqualTo("password", message="密码不一致！")])