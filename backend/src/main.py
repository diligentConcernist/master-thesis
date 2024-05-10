from authlib.integrations.flask_oauth2 import ResourceProtector
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from .auth import Auth0JWTBearerTokenValidator
from .entities.book import Book, BookSchema
from .entities.entity import Session, engine, Base
from .env import AUTH0_DOMAIN, AUD

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(AUTH0_DOMAIN, AUD)
require_auth.register_token_validator(validator)

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)


def drop_table(table_name, engine=engine):
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    if table is not None:
        Base.metadata.drop_all(engine, [table], checkfirst=True)


# drop_table('processed_books', engine)
#
# data = pd.read_csv("G:/Projects/University/m_2/practice/master-thesis/backend/src/data/out.csv", sep=";", encoding='latin-1')
# data.to_sql("processed_books", engine)

@app.route("/books")
def get_books_with_rating():
    session = Session()
    book_objects = session.query(Book).distinct(Book.isbn).limit(20).all()

    schema = BookSchema(many=True)
    books = schema.dump(book_objects)
    response = jsonify(books)
    response.headers.add('Access-Control-Allow-Origin', '*')

    session.close()
    return jsonify(books)


@app.route("/books", methods=["POST"])
@require_auth(None)
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
