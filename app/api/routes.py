import json
from flask import Blueprint, request, jsonify
from helpers import user_token_required, library_token_required, secret_key_required
from models import db, User, Book, Library, Transaction, book_schema, books_schema, library_schema, full_library_schema, libraries_schema, transaction_schema, transactions_schema

api = Blueprint('api', __name__, url_prefix='/api')

# User routes
@api.route('/user/<book_id>', methods=['PUT'])
@user_token_required
def add_user(current_user_token, book_id):
    book = Book.query.get(book_id)
    book.user_id = current_user_token.id
    book.in_stock = False
    
    db.session.commit()
    
    response = book_schema.dump(book)
    return jsonify(response)
    


# Books routes
# GET 
@api.route('/books', methods=['GET'])
def all_books():
    books = Book.query.all()
    response = books_schema.dump(books)
    return jsonify(response)
    

@api.route('/books/user')
@user_token_required
def user_books(current_user_token):
    user = current_user_token.id
    books = Book.query.filter_by(user_id = user).all()
    response = books_schema.dump(books)
    return jsonify(response)


# POST
@api.route('/books', methods=['POST'])
@library_token_required
def create_book(current_library_token):
    title = request.json['book_title']
    isbn = request.json['isbn']
    pages = request.json['pages']
    language = request.json['language']
    genre = request.json['genre']
    author = request.json['author']
    token = current_library_token.library_token
 
    
    book = Book(title, isbn, pages, language, genre, author, token)
    
    db.session.add(book)
    db.session.commit()
    
    response = book_schema.dump(book)
    return jsonify(response)

# PUT
@api.route('/books/<id>', methods=['PUT'])
@library_token_required
def change_book(current_library_token, id):
    book = Book.query.get(id)
    book.book_title = request.json['book_title']
    book.isbn = request.json['isbn']
    book.pages = request.json['pages']
    book.language = request.json['language']
    book.genre = request.json['genre']
    book.author = request.json['author']
    if request.json['library_token']:
        book.token = request.json['library_token']

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# DELETE
@api.route('/books/<id>', methods = ['DELETE'])
@library_token_required
def delete_book(current_library_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)
    



# Library routes
# GET
@api.route('/library')
@secret_key_required
def libraries(current_secret_key):
    libraries = Library.query.all()
    response = libraries_schema.dump(libraries)
    return jsonify(response)

# POST
@api.route('/library', methods=['POST'])
@secret_key_required
def create_library(current_secret_key):
    name = request.json['library_name']
    email = request.json['library_email']
    address = request.json['library_address']
    city = request.json['library_city']
    state = request.json['library_state']
    password = request.json['library_password']
    
    library = Library(name, email, address, city, state, library_password=password)
    
    db.session.add(library)
    db.session.commit()
    
    response = full_library_schema.dump(library)
    return jsonify(response)

# PUT
@api.route('/library/<id>', methods=['PUT'])
@library_token_required
def change_library(current_library_token, id):
    library = Library.query.get(id)
    library.library_name = request.json['library_name']
    library.library_email = request.json['library_email']
    library.library_address = request.json['library_address']
    library.library_city = request.json['library_city']
    library.library_state = request.json['library_state']

    db.session.commit()
    
    response = full_library_schema.dump(library)
    return jsonify(response)

# DELETE
@api.route('/library/<id>', methods=['DELETE'])
@secret_key_required
def delete_library(current_secret_key, id):
    library = Library.query.get(id)
    db.session.delete(library)
    db.session.commit()
    
    response = library_schema.dump(library)
    return jsonify(response)

# Transaction routes
# GET
@api.route('/transactions/library/<id>')
@library_token_required
def library_transactions(current_library_token, id):
    library = current_library_token.library_id
    transactions = Transaction.query.filter_by(library_id = library).all()
    
    response = transactions_schema.dump(transactions)
    return jsonify(response)

@api.route('/transactions/user/<id>')
@user_token_required
def user_transactions(current_library_token, id):
    transactions = Transaction.query.filter_by(user_id = id).all()
    response = transactions_schema.dump(transactions)
    return jsonify(response)


# POST
@api.route('/transactions/<id>', methods=['POST'])
@user_token_required
def create_transaction(current_user_token, id):
    book = Book.query.filter_by(book_id = request.json['book_id']).first()
    if book.in_stock == False and request.json['checking_out'] == True:
        return {'message': 'book is out of stock'}
    if book.in_stock == True and request.json['checking_out'] == False:
        return {'message': 'book has already been returned'}
    
    user_id = id
    book_id = request.json['book_id']
    library_id = request.json['library_id']
    user_token = request.json['user_token']
    checking_out = request.json['checking_out']
    
    if request.json['checking_out'] == True:
        book.in_stock = False
    else:
        book.in_stock = True
    
    transaction = Transaction(user_id, book_id, library_id, user_token, checking_out)
    
    db.session.add(transaction)
    db.session.commit()
    
    response = transaction_schema.dump(transaction)
    return jsonify(response)

# DELETE
@api.route('/transactions/<id>')
@library_token_required
def delete_transaction(current_library_token, id):
    transaction = Transaction.query.get(id)
    
    db.session.delete(transaction)
    db.session.commit()
    
    response = transaction_schema.dump(transaction)
    return jsonify(response)
