
"""
Index
"""


from flask import render_template
from app.tailor import tailor_views
from app.auth.decorators import tailor_required


@tailor_views.route("/dashboard")
@tailor_required
def dashboard():
    return render_template('pages/home.html',
                           page='dashboard')


@tailor_views.route("/account")
@tailor_required
def account():
    return render_template('pages/tailor/account.html',
                           page='account')

@tailor_views.route("/my_products")
@tailor_required
def get_all_products():
    return render_template('pages/tailor/products.html',
                           page='my products')
