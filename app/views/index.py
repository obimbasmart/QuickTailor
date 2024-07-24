
"""
Index
"""


from flask_login import current_user
from flask import render_template, request, jsonify, redirect, url_for
from app.views import app_views
from app.db_access.product import _get_products
from app.models.order import Order
from app.models.tailor import Tailor
from app.models.review import Review




@app_views.route("/")
def home():
    products = _get_products()
    if not current_user.is_anonymous and current_user.is_tailor:
        products = [product.id for product in current_user.products]
        orders = Order.query.all()
        my_orders = [
            order for order in orders
            if order.product_id in products
        ]
        return render_template('pages/tailor/dashboard.html',
                           page='dashboard', orders = my_orders)


    # get popular tailors
    tailors = Tailor.query.filter(Tailor.business_name != None).all()
    reviews = Review.query.filter(Review.rating >= 4).all()
    return render_template('pages/home.html',
                           page='home',
                           products=products, 
                           tailors=tailors, reviews=reviews)

@app_views.route("/how-it-works")
def how_it_works():
    return render_template('pages/howItWorks.html',page='how it works')


@app_views.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('app_views.home'))
    return render_template('pages/register.html',page='auth_page')

@app_views.route('/about')
def about_us():
    return render_template('pages/about_us.html')



