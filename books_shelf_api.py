from book_model import db, Book
from flask import Flask, request
from dotenv import load_dotenv
import os
from flask import jsonify
from sqlalchemy import or_

app = Flask(__name__)

load_dotenv(dotenv_path="./key.env")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db.init_app(app)

@app.route("/books", methods=["GET"])
def books()->Book:
    results = db.session.execute(db.select(Book)).scalars()
    books = [{"id":result.id, "title":result.title, "author":result.author, "rating":result.rating}
            for result in results]
    return jsonify(books=books)
@app.route("/books/<int:id>", methods=["GET"])
def get_book(id)->Book:
    book = db.session.execute(db.select(Book).filter_by(id=id)).scalar_one()
    return jsonify(book=book.get_dict()), 200
@app.route("/books/create-book/", methods=["POST"])
def add_book()->Book:
    title = request.form.get("title")
    author = request.form.get("author")
    rating = int(request.form.get("rating"))
    book =Book(title=title, author=author, rating=rating)
    try:
            db.session.add(book)
            db.session.commit()
    except Exception as e:
            db.session.rollback()
            return f"Exception {e}"
    return jsonify(response=book.get_dict()), 308
@app.route("/books/search-book/")
def search_book()->Book:
    q= request.form.get("q").title()
    db.session.expire_all()
    books = Book.query.filter( or_(
        Book.title.ilike(f"%{q}%"),
        Book.author.ilike(f"%{q}%"),
    ) ).all()
    print(books)
    return jsonify(books=[book.get_dict() for book in books]), 200
if __name__ == "__main__":
    app.run(debug=True, port=5001)