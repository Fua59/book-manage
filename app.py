from datetime import datetime

from flask import Flask, render_template, request, redirect, session, g
from flask_migrate import Migrate
from sqlalchemy import func

import config
from exts import db
from Blueprints.auth import bp as auth_bp
from Blueprints.manager import bp as manager_bp
from Blueprints.user import bp as user_bp
from models import User, Borrow

app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(manager_bp, url_prefix='/manager')
app.register_blueprint(user_bp, url_prefix='/user')

db.init_app(app)

migrate = Migrate(app, db)

# 测试连接
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text('select 1'))
#         print(rs.fetchone())


# 查询cookie中存储的用户并存储为全局变量
@app.before_request
def set_user():
    user = session.get('user')
    if user:
        the_user = User.query.get(user)
        setattr(g, 'user', the_user)
    else:
        setattr(g, 'user', None)

# 查询cookie中存储的今日归还数并存储为全局变量
@app.before_request
def set_count():
    # 如果用户已登录
    if 'user' in session:
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        count = (
            Borrow.query
            .filter(
                Borrow.user_id == session['user'],
                Borrow.deadline <= today_end
            )
            .with_entities(func.count(Borrow.id).label('overdue_count'))
            .scalar()
        )
        setattr(g, 'count', count)  # 存入 g
        session['count'] = count  # 存入 session
    else:
        setattr(g, 'count', None)

# 上下文处理器
@app.context_processor
def user_processor():
    return {'user': g.user, 'count': g.count}

if __name__ == '__main__':
    app.run(debug=True)
