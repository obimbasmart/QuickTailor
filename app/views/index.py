
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


notification= [
    {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "10, 000"},
      {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "30,000"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "200, 000"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "1, 000, 000"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
    {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"}

]


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
    tailors = Tailor.query.all()
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

@app_views.route('/get_notifications')
def get_notifications():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_notifications = notification[start:end]
    return jsonify(paginated_notifications)

@app_views.route('/notification')
def notificationn():
    return render_template("pages/notification.html")



