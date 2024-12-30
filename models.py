from exts import db

class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(50), nullable=False)
    book_author = db.Column(db.String(50), nullable=False)

    # 外键
    booktype_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)

    # 关系
    type = db.relationship('Type', backref='books', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    privilege = db.Column(db.Boolean, nullable=False, default=False)

class Borrow(db.Model):
    __tablename__ = 'borrows'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_time = db.Column(db.DateTime, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    # 关系
    user = db.relationship("User", backref="borrows", lazy=True)
    book = db.relationship("Book", backref="borrow", uselist=False, lazy=True)