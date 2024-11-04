import os
from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from book_form import AddBookForm
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import book_model
app = Flask(__name__)
db = book_model.db
load_dotenv(dotenv_path="./key.env")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db.init_app(app)
with app.app_context():
    db.create_all()



bootstrap = Bootstrap5(app)
all_books = []

@app.route("/")
def index():
    return render_template("home.html", books=all_books)

@app.route("/books/create", methods=['GET','POST'])
def add_a_book():
    form = AddBookForm()
    if form.validate_on_submit():
        title = form.book_name.data
        author = form.author.data
        rating = int(form.rating.data)
        new_book = {"title": title, "author":author, "rating":rating}
        all_books.append(new_book)
        return redirect(url_for("success", title=title))
    return render_template('add_book.html', form=form)

@app.route("/success/<title>", methods=["GET"])
def success(title):
    return render_template("success.html", title=title)
if __name__ == "__main__":
    app.run(debug=True)