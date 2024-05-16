

'''App forms'''

from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    SubmitField,
    PasswordField,
    StringField
)
from wtforms.validators import DataRequired, Email, Length


class CreateProductForm(FlaskForm):
    file = FileField("Choose file")
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Submit')
