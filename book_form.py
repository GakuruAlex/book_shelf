from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class AddBookForm(FlaskForm):
    book_name = StringField(label="Book Name" , validators=[DataRequired()])
    author = StringField(label="Author", validators=[DataRequired()])
    rating = StringField(label="Rating", validators=[DataRequired()])
    add_book = SubmitField(label="Add Book", render_kw={"class":"btn btn-primary"} )