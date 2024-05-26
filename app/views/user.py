

from flask import render_template
from app.views import app_views
from app.forms.main_forms import MeasurementForm

@app_views.route('/yomi-casual')
def tailor_profile():
    return render_template('pages/tailor_profile.html')

@app_views.route('/measurement', methods=["GET","POST"])
def get_set_measurement():
    form = MeasurementForm()
    if form.validate_on_submit():
        return "Submitted"
    return render_template('pages/measurements.html',
                           form=form)