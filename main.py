import os
from flask import Flask, render_template
from book_form import AddBookForm
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv(dotenv_path="./key.env")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

@app.route("/add_book", methods=['GET','POST'])
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        print(form.data)
    return render_template('add_book.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)