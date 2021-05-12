from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from shop.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username'), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^.{6,8}$',
                              message='Your password should be between 6 and 8 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username has already been taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    choices = [('Pen', 'Pen'), ('Pencil', 'Pencil'), ('Rubber', 'Rubber'), ('USB', 'USB'), ('Rubber', 'Rubber'), ('Calculator', 'Calculator')]
    select = SelectField('Search item:', choices=choices)
    search = StringField('')

class CheckoutForm(FlaskForm):
    FisrtName = StringField('First Name', validators=[DataRequired('Please enter your First Name'), Length(min=3, max=15)])
    LastName = StringField('Last Name', validators=[DataRequired('Please enter your Last Name'), Length(min=3, max=15)])
    Adress = StringField('Address', validators=[DataRequired('Please enter your Address')])
    Card_No = PasswordField('Card_No', validators=[DataRequired('Please enter your 16-digit card number'), Length(min=16, max=16)])
    CVC = PasswordField('CVC', validators=[DataRequired('Please enter your 3-digit CVC'), Length(min=3, max=3)])
    Submit = SubmitField('Checkout')
