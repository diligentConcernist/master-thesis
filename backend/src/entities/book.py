from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, Float

from .entity import Base


class Book(Base):
    __tablename__ = "processed_books"

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    isbn = Column(String)
    book_title = Column(String)
    book_author = Column(String)
    year_of_publication = Column(Integer)
    publisher = Column(String)
    image_url = Column(String)
    book_rating = Column(Float)

    def __init__(self, isbn, book_title, book_author, year_of_publication, publisher, image_url, book_rating):
        self.isbn = isbn
        self.book_title = book_title
        self.book_author = book_author
        self.year_of_publication = year_of_publication
        self.publisher = publisher
        self.image_url = image_url
        self.book_rating = book_rating


class BookSchema(Schema):
    id = fields.Number(dump_only=True)
    isbn = fields.Str()
    book_title = fields.Str()
    book_author = fields.Str()
    year_of_publication = fields.Number()
    publisher = fields.Str()
    image_url = fields.Str()
    book_rating = fields.Number()
