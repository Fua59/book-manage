from datetime import datetime, timedelta
from flask import Blueprint, request, session, redirect, render_template, url_for, g, jsonify
from sqlalchemy import case, func
from models import Type, Book, Borrow
from exts import db
from decorators import login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/main', methods=['POST', 'GET'])
@login_required
def main():
    now = datetime.now()
    user_borrow = Borrow.query.filter_by(user_id=session.get('user')).order_by(Borrow.deadline.asc()).all()

    return render_template("main.html", borrows=user_borrow, now=now)


@bp.route('/s&b', methods=['POST', 'GET'])
@login_required
def sb():
    return render_template('s&b.html')


@bp.route('/search')
@login_required
def search():
    now = datetime.now()
    option = request.args.get('option')
    keyword = request.args.get('keywords')

    # 按名称搜索
    if option == '0':
        # 查询图书及其借用情况
        books = (
            Book.query
            .filter(Book.book_name.contains(keyword))  # 根据书名关键字过滤
            .order_by(
                case(
                    (Book.borrow == None, 0),  # 可借阅（没有 Borrow 记录）
                    else_=1  # 不可借阅（有 Borrow 记录）
                ).asc(),  # 按是否可以借阅排序（可借阅在前，不可借阅在后）
                Book.id.asc()  # 按图书 ID 升序排序
            )
            .all()
        )
        return render_template('s&b.html', books=books, now=now)
    # 按类型
    elif option == '1':
        books = (
            Book.query.join(Type)
            .filter(Type.name.contains(keyword))  # 根据书名关键字过滤
            .order_by(
                case(
                    (Book.borrow == None, 0),  # 可借阅（没有 Borrow 记录）
                    else_=1  # 不可借阅（有 Borrow 记录）
                ).asc(),  # 按是否可以借阅排序（可借阅在前，不可借阅在后）
                Book.id.asc()  # 按图书 ID 升序排序
            )
            .all()
        )
        return render_template('s&b.html', books=books, now=now)

    return render_template('s&b.html', now=now)

@bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow(book_id):
    now = datetime.now()
    ddl = now + timedelta(days=7)
    new_borrow = Borrow(borrow_time=now, deadline=ddl, book_id=book_id, user_id=session.get('user'))
    db.session.add(new_borrow)
    db.session.commit()
    return jsonify({'message': 'success'})

@bp.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def returnbook(borrow_id):
    the_borrow = Borrow.query.get(borrow_id)
    if the_borrow is None:
        return jsonify({'message': 'failed'})
    else:
        db.session.delete(the_borrow)
        db.session.commit()
        return jsonify({'message': 'success'})