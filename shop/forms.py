from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from shop.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired("Please enter your first name"), Length(min=3, max=15)])
    surname = StringField('Surname', validators=[DataRequired("Please enter your surname"), Length(min=3, max=15)])
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
            raise ValidationError('Username already exist. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class takeTestForm(FlaskForm):
    question1 = StringField('Question 1', validators=[DataRequired("Please answer question 1"), Length(min=1)])
    question2 = StringField('Question 2', validators=[DataRequired("Please answer question 2"), Length(min=1)])
    question3 = StringField('Question 3', validators=[DataRequired("Please answer question 3"), Length(min=1)])
    question4 = StringField('Question 4', validators=[DataRequired("Please answer question 4"), Length(min=1)])
    question5 = StringField('Question 5', validators=[DataRequired("Please answer question 5"), Length(min=1)])
    question6 = StringField('Question 6', validators=[DataRequired("Please answer question 6"), Length(min=1)])
    question7 = StringField('Question 7', validators=[DataRequired("Please answer question 7"), Length(min=1)])
    question8 = StringField('Question 8', validators=[DataRequired("Please answer question 8"), Length(min=1)])
    question9 = StringField('Question 9', validators=[DataRequired("Please answer question 9"), Length(min=1)])
    question10 = StringField('Question 10', validators=[DataRequired("Please answer question 10"), Length(min=1)])

    submit = SubmitField('Submit Test')
