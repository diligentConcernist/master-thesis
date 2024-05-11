import pandas as pd
from authlib.integrations.flask_oauth2 import ResourceProtector
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import func

from .auth import Auth0JWTBearerTokenValidator
from .entities.book import Book, BookSchema
from .entities.entity import Session, engine, Base
from .entities.popular_book import PopularBook, PopularBookSchema
from .entities.rated_book import RatedBook, RatedBookSchema
from .env import AUTH0_DOMAIN, AUD

RARE_NUMBER_OF_VOTES = 50

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(AUTH0_DOMAIN, AUD)
require_auth.register_token_validator(validator)

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)

# drop_table('popular_books', engine)
# data = pd.read_csv("G:/Projects/University/m_2/practice/master-thesis/backend/src/data/out.csv", sep=";",
# encoding='latin-1')
# data.to_sql("processed_books", engine)
# popular_books = pd.read_csv("G:/Projects/University/m_2/practice/master-thesis/backend/src/data/popular_books.csv",
# sep=";", encoding='latin-1')
# popular_books.to_sql("popular_books", engine)

# drop_table('rated_books', engine)
# rated_books = pd.read_csv("G:/Projects/University/m_2/practice/master-thesis/backend/src/data/rated_books.csv",
#               sep=";", encoding='latin-1')
# rated_books.to_sql("rated_books", engine)

raw_data = pd.read_csv("G:/Projects/University/m_2/practice/master-thesis/backend/src/data/raw_data.csv", sep=";",
                       encoding='latin-1')


@app.route("/popular_books")
def get_popular_books():
    session = Session()
    book_objects = session.query(PopularBook).limit(10).all()

    schema = PopularBookSchema(many=True)
    books = schema.dump(book_objects)
    response = jsonify(books)
    response.headers.add('Access-Control-Allow-Origin', '*')

    session.close()
    return jsonify(books)


@app.route("/search_books")
def search_books():
    session = Session()
    search = request.args.get("search")
    book_objects = session.query(RatedBook).filter(func.lower(RatedBook.book_title).contains(func.lower(search))).limit(
        20).all()

    schema = RatedBookSchema(many=True)
    books = schema.dump(book_objects)
    response = jsonify(books)
    response.headers.add('Access-Control-Allow-Origin', '*')

    session.close()
    return jsonify(books)


@app.route("/book")
def get_book_and_recommendations():
    session = Session()
    title = request.args.get("title")
    schema = RatedBookSchema(many=True)

    book_object_count = session.query(RatedBook).filter_by(book_title=title).first().number_of_votes

    if book_object_count < RARE_NUMBER_OF_VOTES:
        common_books = session.query(RatedBook).filter(RatedBook.number_of_votes > RARE_NUMBER_OF_VOTES).order_by(
            func.random()).limit(5)
        books = schema.dump(common_books)
        resp = jsonify(recommended_books=books, is_rare_book=True)
        resp.headers.add('Access-Control-Allow-Origin', '*')

        session.close()
        return resp

    rating_count = pd.DataFrame(raw_data["book_title"].value_counts())
    rare_books = rating_count[rating_count[rating_count.columns[0]] <= RARE_NUMBER_OF_VOTES].index
    common_books = raw_data[~raw_data["book_title"].isin(rare_books)]
    common_books_pivot = common_books.pivot_table(index=["user_id"], columns=["book_title"], values="book_rating")
    book_title = common_books_pivot[title]
    book_title = book_title.sort_values(ascending=False).dropna()
    recommendation_df = pd.DataFrame(common_books_pivot.corrwith(book_title).sort_values(ascending=False)).reset_index(
        drop=False).dropna()

    if title in [book_title for book_title in recommendation_df["book_title"]]:
        recommendation_df = recommendation_df.drop(recommendation_df[recommendation_df["book_title"] == title].index[0])

    less_rating = []
    for i in recommendation_df["book_title"]:
        if raw_data[raw_data["book_title"] == i]["book_rating"].mean() < 5:
            less_rating.append(i)
    if recommendation_df.shape[0] - len(less_rating) > 5:
        recommendation_df = recommendation_df[~recommendation_df["book_title"].isin(less_rating)]

    recommendation_df = recommendation_df[0:5]["book_title"].values.tolist()
    book_objects = session.query(RatedBook).filter(RatedBook.book_title.in_(recommendation_df)).all()

    books = schema.dump(book_objects)
    resp = jsonify(recommended_books=books, is_rare_book=False)
    resp.headers.add('Access-Control-Allow-Origin', '*')

    session.close()
    return resp


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
