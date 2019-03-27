from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from shop.models import User


class cardEntry(FlaskForm):
    cardName = StringField('Card First Name', validators=[DataRequired('Please enter your first name'), Regexp('^([A-Z][a-zA-Z]*)',
     message='No numbers and capitilised name') ,Length(min=2, max=20,
     message='Name must be between 2 and 20 characters')], render_kw={"Placeholder": 'Name'})
    cardNumber = StringField('Card Number', validators=[DataRequired('Please enter your card number'), 
        Regexp('^\d{19}$', message='Card numbers are 19 digits long')])
    expiryMonth = StringField('Expiry Month',
        validators=[DataRequired('Please enter the expiry month'), 
        Regexp('^([1-9]|1[012])$', message='Number needs to be between 1-12')], render_kw={"Placeholder": '1/12'})
    expiryYear = StringField('Expiry Year', validators=[DataRequired('Please enter expiry year'),
        Regexp('^[9]{1}$|^[1-3]{1}[0-6]{1}$|^36$',   
        message='Number must be between 9-36')], render_kw={"Placeholder": '9/36'})
    CVV = StringField('CVV', validators=[DataRequired('Enter CVV'), Regexp('^\d{3}$', 
        message='CVV is only 3 digits ')])
    submit = SubmitField('Complete purchase')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username'), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^.{4,12}$',
                              message='Your password should be between 4 and 12 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exist. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
