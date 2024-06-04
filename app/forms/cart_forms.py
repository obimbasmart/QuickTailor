'''App Auth forms'''

from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    BooleanField
)
from wtforms.validators import (DataRequired, 
                                ValidationError)
from ..models.user import User
from ..models.tailor import Tailor



class CustomizationForm(FlaskForm):
    code = StringField('Customization code', validators=[DataRequired()])
    submit = SubmitField('Apply')

    def validate_coce(self,code):
        if code != "QuicTailor":
            raise ValidationError("Invalid code")
        
class ApplyCodeForm(FlaskForm):
    code = StringField(validators=[DataRequired()])
    apply = SubmitField('Apply')


class Checkout(FlaskForm):
    submit = SubmitField('Checkout')

    def validate_coce(self,code):
        if code != "QuicTailor":
            raise ValidationError("Invalid code")
