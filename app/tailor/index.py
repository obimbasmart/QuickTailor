
"""
Index
"""


from flask import render_template, redirect, url_for
from app.tailor import tailor_views
from app.auth.decorators import tailor_required
from app.models.product import Product
from app.forms.tailor_forms import CRSForm
from flask_login import current_user
from app import s3_client

@tailor_views.route("/dashboard")
@tailor_required
def dashboard():
    return render_template('pages/home.html',
                           page='dashboard')


@tailor_views.route("/dashboard")
@tailor_required
def profile():
    return render_template('pages/home.html',
                           page='dashboard')


@tailor_views.route("/account")
@tailor_required
def account():
    return render_template('pages/tailor/account.html',
                           page='account')