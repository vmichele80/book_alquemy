import os

from flask import Flask, flash, redirect, render_template, request, url_for

from data_models import Author, Book, db

app = Flask(__name__)   # Create Flask app

# Creating a key to control the session in order to show the message on the page
app.config["SECRET_KEY"] = "dev_key_for_library_app"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """This endpoint adds an author on Post, checking if name is unique.
    on GET it retrieves the page UI to add an author
    """
    if request.method == 'POST':

        name = request.form["name"].strip()
        birthdate = request.form.get("birthdate")
        date_of_death = request.form.get("date_of_death")

        if not name:
            flash("Author name cannot be empty.")
            return redirect(url_for("add_author"))

        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            flash(f'Author "{name}" already exists.')
            return redirect(url_for("add_author"))

        author = Author(
            name = name,
            birth_date =  birthdate,
            date_of_death = date_of_death)

        db.session.add(author)
        db.session.commit()

        flash (f"Author  - { author.name } - has been added")

        return redirect(url_for("add_author"))

    else:
    # It must be a get method
        return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """This endpoint add books. on get it retrieves the page
    on POST it stores the data a redirect to homepage"""

    if request.method == 'POST':

        title = request.form["title"].strip()
        isbn = request.form.get("isbn", "").strip()
        publication_year = request.form.get("publication_year")
        publication_year = int(publication_year) if publication_year else None
        author_id = int(request.form["author_id"])

        if not title:
            flash("Book title cannot be empty.")
            return redirect(url_for("add_book"))

        if isbn:
            existing_book = Book.query.filter_by(isbn=isbn).first()
            if existing_book:
                flash(f'ISBN "{isbn}" already exists.')
                return redirect(url_for("add_book"))
        else:
            isbn = None

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
    # It must be a get method
        authors = Author.query.all()
        return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a specific book from the database."""

    book = Book.query.get_or_404(book_id)
    author = book.author
    book_title = book.title

    db.session.delete(book)
    db.session.commit()

    if author and len(author.books) == 0:
        author_name = author.name
        db.session.delete(author)
        db.session.commit()

        flash(
            f'Book "{book_title}" was deleted. Author "{author_name}" '
            'was also deleted because there are no more books by that author.'
        )
    else:
        flash(f'Book "{book_title}" was deleted successfully.')

    return redirect(url_for('books_list'))

@app.route('/', methods=['GET'])
def books_list():
    """Show the full list of books, sortable by title or author."""
    sort = request.args.get("sort", "title")

    # Need to catch the search argument if passed
    search = request.args.get("search", "").strip()

    if sort == "author":
        books_query  = Book.query.join(Author).order_by(Author.name.asc())
    else:
        books_query  = Book.query.order_by(Book.title.asc())

    if search:
        books_query = books_query.filter(Book.title.ilike(f"%{search}%"))

    books = books_query.all()

    return render_template('home.html', books=books, sort=sort, search=search)


# This is the code to generate the tables. Commented out after the first run
"""
with app.app_context():
  db.create_all()
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)