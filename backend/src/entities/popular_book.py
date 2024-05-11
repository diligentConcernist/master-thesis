from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, Float

from .entity import Base


class PopularBook(Base):
    __tablename__ = "popular_books"

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    book_title = Column(String)
    number_of_votes = Column(Integer)
    average_ratings = Column(Float)
    popularity = Column(Float)
    image_url = Column(String)

    def __init__(self, isbn, book_title, number_of_votes, average_ratings, popularity, image_url):
        self.isbn = isbn
        self.book_title = book_title
        self.number_of_votes = number_of_votes
        self.average_ratings = average_ratings
        self.popularity = popularity
        self.image_url = image_url


class PopularBookSchema(Schema):
    id = fields.Number(dump_only=True)
    book_title = fields.Str()
    number_of_votes = fields.Integer()
    average_ratings = fields.Float()
    popularity = fields.Float()
    image_url = fields.Str()