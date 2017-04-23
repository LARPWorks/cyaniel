# Imports
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
import datetime

from ..models import User


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account

    """
    # List of tuple objects for birthday validation
    current_year = datetime.datetime.now().year
    birth_days = [(n, n) for n in range(1, 32)]
    birth_years = [(n, n) for n in range(1950, current_year + 1)]

    # Fields for User registration form
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_name = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirm Password')
    phone = StringField('Phone Number', validators=[DataRequired()])
    birth_month = SelectField(u'Birth Month',
                              choices=[('01', 'January'), ('02', 'February'), ('03', 'March'),
                                       ('04', 'April'), ('05', 'May'), ('06', 'June'),
                                       ('07', 'July'), ('08', 'August'), ('09', 'September'),
                                       ('10', 'October'), ('11', 'November'), ('02', 'December')],
                              validators=[DataRequired()])
    birth_day = SelectField(u'Birth Day',
                            choices=birth_days, coerce=int,
                            validators=[DataRequired()])
    birth_year = SelectField(u'Birth Year',
                             choices=birth_years, coerce=int,
                             validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    emergency_contact_name = StringField('Emergency Contact', validators=[DataRequired()])
    emergency_contact_number = StringField('Emergency Contact Number', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')