from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import declarative_base, sessionmaker

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    birth_date = db.Column(db.String) # this date might be unknown
    date_of_death = db.Column(db.String) # this date might be unknown

    books = db.relationship('Book', back_populates='author', lazy=True)

    def __repr__(self):
        return f"{self.id} Author name: {self.name}, born on {self.birth_date}, died on {self.date_of_death}"

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20),unique=True) #older books do not have an isbn
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id') )

    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f"{self.id} Book title: {self.title}, published on {self.publication_year}. ISBN code: {self.isbn}"

    def __str__(self):
        return self.title


