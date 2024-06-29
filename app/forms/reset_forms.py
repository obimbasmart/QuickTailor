'''App forms'''

from app.models import db
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
                                Email, EqualTo,
                                ValidationError)
from ..models.user import User
from ..models.tailor import Tailor


class ResetEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).one_or_none()
        tailor = Tailor.query.filter_by(email=email.data).one_or_none()
        if user is None and tailor is None:
            raise ValidationError("Email not registered")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')
