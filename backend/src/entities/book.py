from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer

from .entity import Entity, Base


class Book(Entity, Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    isbn = Column(String)
    book_title = Column(String)
    book_author = Column(String)
    year_of_publication = Column(Integer)
    publisher = Column(String)
    image_url = Column(String)

    def __init__(self, isbn, book_title, book_author, year_of_publication, publisher, image_url, created_by):
        Entity.__init__(self, created_by)
        self.isbn = isbn
        self.book_title = book_title
        self.book_author = book_author
        self.year_of_publication = year_of_publication
        self.publisher = publisher
        self.image_url = image_url


class BookSchema(Schema):
    id = fields.Number(dump_only=True)
    isbn = fields.Str()
    book_title = fields.Str()
    book_author = fields.Str()
    year_of_publication = fields.Number()
    publisher = fields.Str()
    image_url = fields.Str()
