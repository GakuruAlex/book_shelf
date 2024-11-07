from book_model import db, Book
from flask import Flask
from dotenv import load_dotenv
import os
from flask import jsonify

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
    return jsonify(book=book.get_dict())
if __name__ == "__main__":
    app.run(debug=True, port=5001)