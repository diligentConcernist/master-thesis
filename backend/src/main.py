from flask import Flask, jsonify, request
from flask_cors import CORS

from .entities.book import Book, BookSchema
from .entities.entity import Session, engine, Base

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)


@app.route("/books")
def get_books():
    session = Session()
    book_objects = session.query(Book).all()

    schema = BookSchema(many=True)
    books = schema.dump(book_objects)
    response = jsonify(books)
    response.headers.add('Access-Control-Allow-Origin', '*')

    session.close()
    return jsonify(books)


@app.route("/books", methods=["POST"])
def add_book():
    added_book = BookSchema(only=("isbn", "book_title", "book_author",
                                  "year_of_publication", "publisher", "image_url")).load(request.get_json())
    book = Book(**added_book, created_by="HTTP POST Request")

    session = Session()
    session.add(book)
    session.commit()

    new_book = BookSchema().dump(book)
    session.close()
    return jsonify(new_book), 201
