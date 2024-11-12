from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
import email_validator
class AddBookForm(FlaskForm):
    title = StringField(label="Book Name" , validators=[DataRequired()])
    author = StringField(label="Author", validators=[DataRequired()])
    rating = StringField(label="Rating", validators=[DataRequired()])
class SignUpForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()], 
                           render_kw={"placeholder": "Your username", "class":"form-control"})
    email = EmailField(label="Email", validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "Your Email", "class":"form-control"})
    password = PasswordField(label="Password", validators=[
        DataRequired(),
        Length(min= 14, message="Password Should be 14 characters long!")
        ],
        render_kw={"placeholder": "Your password", "class":"form-control"})
    confirm_password = PasswordField(label="Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Confirm password", "class":"form-control"})

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()],
                           render_kw={"placeholder": "Your username", "class":"form-control"})
    password = PasswordField(label="Password", validators=[
        DataRequired(),
        Length(min= 14, message="Password Should be 14 characters long!")
        ],
        render_kw={"placeholder": "Your password", "class":"form-control"})
