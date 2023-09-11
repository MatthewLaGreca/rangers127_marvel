from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Email

class LoginForm(FlaskForm):
    """Form used to login a user"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit= SubmitField('Sign In')

class RegisterForm(FlaskForm):
    """Form used to register a user"""

    first = StringField('First Name')
    last = StringField('Last Name')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    verify_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    profile_image = StringField('Profile Image URL')
    email = StringField('Email', validators=[DataRequired(), Email()])
    p_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Register')

class ComicForm(FlaskForm):
    """Form used to add a comic"""

    title = StringField('Comic Title', validators=[DataRequired()])
    series = StringField('Comic Series', validators=[DataRequired()])
    volume = IntegerField('Volume #', validators=[DataRequired()])
    image = StringField('Comic Book Image URL (Optional)')
    description = StringField('Comic Description (Optional)')
    author = StringField('Author of Comic')
    page_count = StringField('Page count of comic')
    isbn = StringField('ISBN of comic')
    for_sale = BooleanField('Is this comic for sale?')
    price = DecimalField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')
