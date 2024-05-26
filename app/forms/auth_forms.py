'''App Auth forms'''

from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    PasswordField,
    StringField,
    BooleanField
)
from wtforms.validators import (DataRequired, 
                                Email, ValidationError)
from ..models.user import User
from ..models.tailor import Tailor




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).one_or_none()
        tailor = Tailor.query.filter_by(email=email.data).one_or_none()
        if  user is None and  tailor is None:
            raise ValidationError("Email not registered")

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    # last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Create account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).one_or_none()
        tailor = Tailor.query.filter_by(email=email.data).one_or_none()
        if not user is None or not tailor is None:
            raise ValidationError("Email already exist")
