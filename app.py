from data_models import db, Author, Book
from flask import Flask, request, render_template, flash, redirect, url_for

import os

app = Flask(__name__)   # Create Flask app

#creating a key to control the session in order to show the message on the page
app.config["SECRET_KEY"] = "dev_key_for_library_app"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':

        name = request.form["name"]
        birthdate = request.form.get("birthdate")
        date_of_death = request.form.get("date_of_death")

        author = Author(
            name = name,
            birth_date =  birthdate,
            date_of_death = date_of_death)

        db.session.add(author)
        db.session.commit()

        flash (f"Author  - { author.name } - has been added")

        return redirect(url_for("add_author"))

    else:
    # it must be a get method
        return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':

        title = request.form["title"]
        isbn = request.form.get("isbn")
        publication_year = request.form.get("publication_year")
        publication_year = int(publication_year) if publication_year else None
        author_id = int(request.form["author_id"])

        book = Book(
            title = title,
            isbn =  isbn,
            publication_year = publication_year,
            author_id = author_id)

        db.session.add(book)
        db.session.commit()

        flash (f"Book  - { book.title } - has been added")

        return redirect(url_for("add_book"))

    else:
    # it must be a get method
        authors = Author.query.all()
        return render_template('add_book.html', authors=authors)

@app.route('/', methods=['GET'])
def books_list():
    """this api will show the full list of books"""
    books = Book.query.all()
    return render_template('home.html', books=books)


# This is the code to generate the tables. Commented out after the first run
"""
with app.app_context():
  db.create_all()
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)