from functools import wraps
from flask import g, redirect, url_for

# 登录装饰器 用于保障登录才能使用的功能
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return wrapper