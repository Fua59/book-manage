from flask import Blueprint, request, session, redirect, render_template, url_for, g
from models import User
from exts import db
from .forms import RegisterForm, LoginForm, PasswordForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user = form.username.data
            pwd = form.password.data
            res = User.query.filter_by(name=user).first()

            if not res:
                print("用户不存在！")
                return redirect(url_for('auth.login'))

            if check_password_hash(res.password, pwd):
                session['user'] = res.id
                if res.privilege:
                    return redirect(url_for('manager.admin'))
                else:
                    return redirect(url_for('user.main'))
            else:
                print("密码错误！")
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():
            new_user = User(name=form.username.data, password=generate_password_hash(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))
    return render_template('register.html')

@bp.route('/change_pwd', methods=['POST', 'GET'])
def change_pwd():
    if request.method == 'POST':
        form = PasswordForm(request.form)
        if form.validate():
            the_user = User.query.get(session.get('user'))
            new_password = generate_password_hash(form.password.data)
            the_user.password = new_password
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.change_pwd'))
    return render_template('change.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))