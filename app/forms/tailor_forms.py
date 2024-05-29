
'''App forms'''

from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    MultipleFileField,
    SubmitField,
    StringField,
    TextAreaField,
    SelectMultipleField,
    widgets,
    DecimalField,
    HiddenField,
    BooleanField,
    IntegerField
)
from app.constants import categories, gender

from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, file_allowed

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MultiRadioField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.RadioInput()

class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    material = StringField('Material', validators=[DataRequired()])
    price = DecimalField('Price (NGN)', validators=[DataRequired()])
    estimated_tc = IntegerField('Duration (days)',  [DataRequired()])
    categories = MultiCheckboxField('Select a category', choices=categories)
    gender = MultiRadioField("Select Gender", choices=gender)
    images = MultipleFileField("Upload product images",
                               validators=[FileRequired()])
    draft = BooleanField('Move to draft')
    submit = SubmitField('Save and Upload')

class CRSForm(FlaskForm):
    crf_token = HiddenField()