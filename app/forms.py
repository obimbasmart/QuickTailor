

'''App forms'''

from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    SubmitField,
    PasswordField,
    StringField,
    HiddenField,
    RadioField
)
from wtforms.validators import (DataRequired, InputRequired, Email, Regexp, 
        NumberRange, Length)
from flask_wtf.file import FileRequired

class CreateProductForm(FlaskForm):
    file = FileField("Choose file")
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    nin  = StringField('NIN', validators=[InputRequired(), Regexp('^[0-9]*$',
    message= "only number") ])
    nin_slip = FileField("Upload NIN Slip", validators=[FileRequired()])
    hidden = HiddenField("Hidden", validators=[FileRequired()])
    your_photo = FileField("Upload your photo", validators=[FileRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    submit = SubmitField('Submit')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Submit')

