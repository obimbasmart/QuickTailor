
"""
Index
"""

from flask_login import current_user, login_required
from flask import render_template, flash, redirect, url_for
from app.views import app_views
from app.forms.main_forms import MeasurementForm
from app.models import db
from decimal import Decimal


@app_views.route('/measurement', methods=["GET", "POST"])
@login_required
def measurement():
    form = MeasurementForm()
    if form.validate_on_submit():
        new_measurements = {}
        for field_name, field in form.data.items():
            if isinstance(field, Decimal):
                new_measurements[field_name] = float(field)
        current_user.measurements = new_measurements
        db.session.commit()
        flash("Measurement updated")
    return render_template('pages/measurements.html',
                           form=form)
