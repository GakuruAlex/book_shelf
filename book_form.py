from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
class AddBookForm(FlaskForm):
    title = StringField(label="Book Name" , validators=[DataRequired()])
    author = StringField(label="Author", validators=[DataRequired()])
    rating = StringField(label="Rating", validators=[DataRequired()])
class SignUp(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired()])
