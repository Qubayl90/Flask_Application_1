from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

#api = Blueprint('api',__name__, url_prefix='/api')
api = Blueprint('api',__name__, url_prefix='/api')

#test API
@api.route('/getdata')
def getdata():
    return {'test': 'test1'}

#Add A Book
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    book_title = request.json['book_title']
    isbn = request.json['isbn']
    author_name = request.json['author_name']
    no_of_pages = request.json['no_of_pages']
    book_type = request.json['book_type']
    book_language = request.json['book_language']
    book_edition = request.json['book_edition']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(book_title,isbn,author_name,no_of_pages,book_type,book_language,book_edition, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

#Get List of Books
@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

#get details of sepcific book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):    # Currently showing cars of other users as well 
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)


#Update Book details
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.book_title = request.json['book_title']
    book.isbn = request.json['isbn']
    book.author_name = request.json['author_name']
    book.no_of_pages = request.json['no_of_pages']
    book.book_type = request.json['book_type']
    book.book_language = request.json['book_language']
    book.book_edition = request.json['book_edition']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# Delete Specific Book
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)