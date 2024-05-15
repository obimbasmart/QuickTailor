

'''App forms'''

from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    SubmitField
)


class CreateProductForm(FlaskForm):
    file = FileField("Choose file")
    submit = SubmitField('Submit')
