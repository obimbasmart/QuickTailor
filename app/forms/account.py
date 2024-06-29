'''App Auth forms'''

from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    IntegerField,
    PasswordField
)
from wtforms.validators import (DataRequired,
                                Email, Length, EqualTo,
                                ValidationError)

from app.models.user import User
from app.models.tailor import Tailor

class UpdateAccountForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone_no = StringField("Mobile Number", validators=[DataRequired()])
    email = StringField('Email')
    submit = SubmitField('Update')


class ResetEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    otp = IntegerField("OTP", validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).one_or_none()
        tailor = Tailor.query.filter_by(email=email.data).one_or_none()
        if not user is None or not tailor is None:
            raise ValidationError("Email already exist")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    otp = IntegerField("OTP", validators=[DataRequired()])
    submit = SubmitField('Reset')

