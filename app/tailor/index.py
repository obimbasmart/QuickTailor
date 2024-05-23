
"""
Index
"""


from flask import render_template
from app.tailor import tailor_views


@tailor_views.route("/dashboard")
def dashboard():
    return render_template('pages/home.html',
                           page='dashboard')

@tailor_views.route("/account")
def account():
    return render_template('pages/tailor/account.html',
                           page='account')

@tailor_views.route("/my_products")
def get_all_products():
    return render_template('pages/tailor/products.html',
                           page='my products')