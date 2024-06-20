

'''App forms'''

from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    DecimalField,
    IntegerField,
    StringField
)

from wtforms.validators import DataRequired


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

class OrderMeasurementForm(MeasurementForm):
    submit = SubmitField('Add measurement')

class ReviewForm(FlaskForm):
    rating = IntegerField("Rating", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    