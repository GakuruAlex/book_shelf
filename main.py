import os
from flask import Flask, redirect, render_template, url_for, flash,  abort, session, request
from flask_bootstrap import Bootstrap5
from book_form import AddBookForm, SignUpForm, LoginForm
from dotenv import load_dotenv
import book_model
from book_model import Book, User
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
from sqlalchemy import or_
app = Flask(__name__)
db = book_model.db

load_dotenv(dotenv_path="./key.env")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
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
@login_required
def create_book():
    form = AddBookForm()
    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        rating = int(form.rating.data)
        book =  Book(title=title, author=author, rating=rating)
        db.session.add(book)
        db.session.commit()
        flash(f"{title} added successfully!", "success")
        return redirect(url_for("book_detail", id=book.id))
    return render_template('create_book.html', heading="Create Book",url_action=('create_book', 0),form=form)

@app.route("/books/<int:id>/edit", methods=["GET","POST", ])
@login_required
def edit_book(id):
    book = get_book(id)
    if book:
        form = AddBookForm(obj=book)
        if form.validate_on_submit():
            book.title = form.title.data
            book.author = form.author.data
            book.rating = int(form.rating.data)
            db.session.commit()
            flash(f"Book details edited successfully!")
            return redirect(url_for('index'))
        return render_template("create_book.html",heading="Edit Book",url_action=('edit_book', id), form=form)
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
@login_required
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

@app.route("/books/search/")
def search():
        q = request.args.get("search")
        if q == "":
            books = db.session.query(Book).all()
        else:
            books =Book.query.filter(
            or_(
                Book.title.ilike(f"%{q}%"),
                Book.author.ilike(f"%{q}%"),
                Book.rating.ilike(f"%{q}%"),
                )
            ).all()
        return render_template("home.html", books=books)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)
@app.route("/users/signup/", methods=["GET","POST"])
def user_signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        hashed_password = generate_password_hash(password=password, method="scrypt", salt_length=8)
        user = User(username = username, password = hashed_password , email= email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login")), 201
    return render_template("signup.html", form=form)

@app.route("/users/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = db.session.query(User).filter_by(username=username).scalar()
        if check_password_hash(user.get_dict()["password"], password):
            login_user(user)
            flash("Login Success")
            return redirect(url_for("index"))
        abort(401)
        login_manager.login_view("login")
    return render_template("login.html", form=form)

@login_required
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)