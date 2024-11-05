import os
from flask import Flask, redirect, render_template, url_for, flash, session
from flask_bootstrap import Bootstrap5
from book_form import AddBookForm
from dotenv import load_dotenv
import book_model
from book_model import Book
from werkzeug.exceptions import NotFound
app = Flask(__name__)
db = book_model.db

load_dotenv(dotenv_path="./key.env")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db.init_app(app)
with app.app_context():
    db.create_all()

bootstrap = Bootstrap5(app)
def get_book(id):
    try:
        return db.get_or_404(Book, id)
    except NotFound:
        flash(f"Book with id {id} not found!")
        return None
@app.route("/books")
def index():
    books = db.session.query(Book).all()
    return render_template("home.html", books=books)

@app.route("/books/create", methods=['GET','POST'])
def create_book():
    form = AddBookForm()
    if form.validate_on_submit():
        title = form.book_name.data
        author = form.author.data
        rating = int(form.rating.data)
        book =  Book(title=title, author=author, rating=rating)
        db.session.add(book)
        db.session.commit()
        flash(f"{title} added successfully!", "success")
        return redirect(url_for("book_detail", id=book.id))
    return render_template('create_book.html', heading="Create Book ",form=form)
@app.route("/books/<int:id>/edit")
def edit_book(id):
    book = get_book(id)
    if book:
        form = AddBookForm(obj=book)
        if form.validate_on_submit():
            book.title = form.book_name.data
            book.author = form.author.data
            book.rating = int(form.rating.data)
            db.session.add(book)
            db.session.commit()
            flash(f"Book details edited successfully!")
            return redirect(url_for('index'))
        return render_template("create_book.html",heading="Edit Book", form=form)
    else:
        return render_template("error.html")
@app.route("/books/<int:id>", methods=["GET"])
def book_detail(id):
    book = get_book(id)
    if book:
        message = session.pop("message", None)
        if message:
            flash(message)
        return render_template("book_detail.html",book=book)
    return render_template('error.html')
@app.route("/books/<int:id>/delete", methods=["GET","POST"])
def delete_book(id):
        book = db.get_or_404(Book, id)
        if book:
            try:
                db.session.delete(book)
                flash(f"{book.title} deleted!")
                db.session.commit()
                return redirect(url_for('index'))
            except Exception as e:
                flash(f"{e}")
                db.session.rollback()
                return redirect(url_for('index'))
        else:
            return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)