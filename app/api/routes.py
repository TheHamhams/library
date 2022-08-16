from flask import Blueprint, request, jsonify
from helpers import user_token_required, library_token_required, secret_key_required
from models import db, User, Book, Library, Transaction, book_schema, books_schema, library_schema, full_library_schema, libraries_schema

api = Blueprint('api', __name__, url_prefix='/api')

# User routes
@api.route('/user/<book_id>', methods=['PUT'])
@user_token_required
def add_user(current_user_token, book_id):
    book = Book.query.get(book_id)
    book.user_id = current_user_token.id
    
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