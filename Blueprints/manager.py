from datetime import datetime
from flask import Blueprint, request, session, redirect, render_template, g, url_for, jsonify
from models import Type, Book, Borrow
from exts import db
from decorators import login_required

bp = Blueprint('manager', __name__, url_prefix='/manager')


@bp.route('/admin')
@login_required
def admin():
    now = datetime.now()
    borrows = Borrow.query.order_by(Borrow.deadline.asc()).all()
    return render_template('admin.html', borrows=borrows, now=now)


@bp.route('/bookadmin')
@login_required
def bookadmin():
    types = Type.query.all()

    return render_template('bookadmin.html', types=types)


@bp.route('/addbook', methods=['POST'])
def addbook():
    data = request.json
    new_book = Book(book_name=data['name'], book_author=data['author'], booktype_id=data['type'])
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'success'})


@bp.route('/addtype', methods=['POST'])
def addtype():
    data = request.json
    new_type = Type(name=data['name'])
    db.session.add(new_type)
    db.session.commit()

    return jsonify({'message': 'success', 'id': new_type.id, 'name': new_type.name})


@bp.route('/deltype/<int:type_id>', methods=['DELETE'])
def deltype(type_id):
    the_type = Type.query.get(type_id)
    db.session.delete(the_type)
    db.session.commit()
    print("deleting!")
    return jsonify({'message': 'success'})

@bp.route('/search')
@login_required
def search():
    now = datetime.now()
    types = Type.query.all()
    option = request.args.get('option')
    keyword = request.args.get('keywords')

    # 名称
    if option == '0':
        books = Book.query.filter(Book.book_name.contains(keyword)).order_by(Book.id.asc()).all()
        return render_template('bookadmin.html', books=books, types=types, now=now)
    # 类型
    elif option == '1':
        books = Book.query.join(Type).filter(Type.name.contains(keyword)).order_by(Book.id.asc()).all()
        return render_template('bookadmin.html', books=books, types=types, now=now)

    return render_template('bookadmin.html', types=types, now=now)

@bp.route('/delbook/<int:book_id>', methods=['DELETE'])
def delbook(book_id):
    the_book = Book.query.get(book_id)
    db.session.delete(the_book)
    db.session.commit()
    print("deleting!")
    return jsonify({'message': 'success'})

@bp.route('/editbook', methods=['POST'])
def editbook():
    data = request.json
    print(data)
    the_book = Book.query.get(data['id'])
    if the_book:
        the_book.book_name = data['name']
        the_book.book_author = data['author']
        the_book.booktype_id = data['type']
        db.session.commit()
        return jsonify({'message': 'success'})
    return jsonify({'message': 'error'})