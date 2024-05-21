

'''App forms'''

from app import db
from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    SubmitField,
    PasswordField,
    StringField,
    DecimalField,
    BooleanField
)
from wtforms.validators import (DataRequired, 
                                Email,
                                ValidationError)
from .models.user import User
from .models.tailor import Tailor


class CreateProductForm(FlaskForm):
    file = FileField("Choose file")
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    # last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Create account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).one_or_none()
        tailor = User.query.filter_by(email=email.data).one_or_none()
        if not user is None or not tailor is None:
            raise ValidationError("Email already exist")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class MeasurementForm(FlaskForm):
    top_length = DecimalField("Top Length", places=2)
    shoulder = DecimalField("Shoulder", places=2)
    sleeve_length = DecimalField("Sleeve Length", places=2)
    neck = DecimalField("Neck", places=2)
    muscle = DecimalField("Muscle", places=2)
    waist = DecimalField("Waist", places=2)
    laps = DecimalField("Laps", places=2)
    knee = DecimalField("Knee", places=2)
    stomach = DecimalField("Stomach", places=2)
    chest_burst = DecimalField("Chest/Burst", places=2)
    submit = SubmitField("Save")
