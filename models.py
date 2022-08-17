from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True, default="")
    last_name = db.Column(db.String(50), nullable=True, default="")
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=True, default="")
    g_auth_verify = db.Column(db.Boolean, default=False)
    user_token = db.Column(db.String, default="", unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    
    def __init__(self, email, first_name='', last_name='', password='', user_token='', g_auth_verify=False):
        self.id = self.set_id()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.user_token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
        
    def set_id(self):
        return str(uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def __repr__(self):
        return f"User {self.email} has been added to the database"
    
class Library(db.Model):
    library_id = db.Column(db.String, primary_key=True)
    library_name = db.Column(db.String(75), nullable=False)
    library_email = db.Column(db.String(50), nullable=False)
    library_password = db.Column(db.String, nullable=True, default='')
    library_address = db.Column(db.String(50), nullable=False)
    library_city = db.Column(db.String(50), nullable=False)
    library_state = db.Column(db.String(30), nullable=False)
    g_auth_verify = db.Column(db.Boolean, default=False)
    library_token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, library_name, library_email, library_address, library_city, library_state, library_password='', library_token='', g_auth_verify=False):
        self.library_id = self.set_id()
        self.library_name = library_name
        self.library_email = library_email
        self.library_password = self.set_password(library_password)
        self.library_address = library_address
        self.library_city = library_city
        self.library_state = library_state
        self.library_token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
        
    def set_id(self):
        return str(uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def __repr__(self):
        return f"Library {self.library_name} has been added to the database"
        

class Book(db.Model):
    book_id = db.Column(db.String, primary_key=True)
    book_title = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=True)
    language = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(20), nullable=True)
    author = db.Column(db.String, nullable=True)
    in_stock = db.Column(db.Boolean, default=True)
    library_token = db.Column(db.String, db.ForeignKey('library.library_token'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, book_title, isbn, pages, language, genre, author, library_token, in_stock=True, user_id=''):
        self.book_id = self.set_id()
        self.book_title = book_title
        self.isbn = isbn
        self.pages = pages
        self.language = language
        self.genre = genre
        self.author = author
        self.in_stock = in_stock
        self.library_token = library_token
        self.userid = user_id
    
    def set_id(self):
        return str(uuid4())
    
    def __repr__(self):
        return f"Book {self.book_title} has been added to the database"
    

class Transaction(db.Model):
    transaction_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)
    book_id = db.Column(db.String, db.ForeignKey('book.book_id'), nullable = False)
    library_id = db.Column(db.String, db.ForeignKey('library.library_id'), nullable = False)
    user_token = db.Column(db.String, db.ForeignKey('user.user_token'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, user_id, book_id, library_id, user_token):
        self.transaction_id = self.set_id()
        self.user_id = user_id
        self.book_id = book_id
        self.library_id = library_id
        self.library_token = user_token
        
    def set_id(self):
        return str(uuid4())
    
    def __repr__(self):
        return f"Transaction {self.transaction_id} has been added to the database"

class LibrarySchema(ma.Schema):
    class Meta:
        fields = ['library_id', 'library_name', 'library_email', 'library_address', 'library_city', 'library_state']

class FullLibrarySchema(ma.Schema):
    class Meta:
        fields = ['library_id', 'library_name', 'library_email', 'library_address', 'library_city', 'library_state', 'library_token']

class BookSchema(ma.Schema):
    class Meta:
        fields = ['book_id', 'book_title', 'isbn', 'pages', 'language', 'genre', 'author', 'in_stock']

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ['transaction_id', 'user_id', 'book_id', 'library_id', 'user_token']

full_library_schema = FullLibrarySchema()
libraries_schema = FullLibrarySchema(many=True)
library_schema = LibrarySchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)