"""
Order views
"""


from flask import render_template, flash
from app.tailor import tailor_views
from app.auth.decorators import tailor_required
from app.forms.tailor_forms import BrandInformationForm
from flask_login import current_user
from app import db, s3_client
from datetime import datetime

# @tailor_views.route("/orders")
# @tailor_required
# def orders():
#     return render_template('pages/tailor/orders.html',
#                            page='orders', )
