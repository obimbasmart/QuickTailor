
"""
Index
"""


from flask_login import current_user
from flask import render_template, request, jsonify
from app.views import app_views
from app.db_access.product import _get_all_products
notification= [
        {"time": "3hr ago", "is_clicked": False, "id": "0","content": "🛍️ Order Confirmation: Your order has been successfully placed!", "icon": "1hr ago", "time_elapsed": "Adegbite concept", "url":"http://localhost:5002/products"},
        {"time": "3hr ago", "is_clicked": True, "id": "1","content": "📦 Order Status Updates: Your order status has been updated to 'In Progress.", "icon": "2 minutes ago", "time_elapsed": "Wellakt Arieie d","url":"http://localhost:5002/messages"},
        {"time": "3hr ago","is_clicked": False, "id": "2", "content": "🌟 Review Request: We hope you enjoyed your tailored experience! Share your feedback and help us improve.", "icon": "📥", "time_elapsed": "2 minutes ago", "url":"http://localhost:5002/"},
        {"time": "3hr ago", "is_clicked": False, "id": "3","content": "💬 Chat Responses: The tailor has replied to your message. Check it out!", "icon":"3 minutes ago", "time_elapsed": "1 day ago", 
            "url": "http://localhost:5002/product/1234"},
        {"time": "3hr ago", "is_clicked": False, "id": "4", "content": "🎁 Promotional Offers: New collection alert! Explore our latest designs with exclusive discounts.", "icon": "📥", "time_elapsed": "2 minutes ago", "url":"http://localhost:5002/messages"}
]


@app_views.route("/")
def home():
    products = _get_all_products()
    return render_template('pages/home.html',
                           page='home',
                           products=products, 
                           current_user=current_user)

@app_views.route("/how-it-works")
def how_it_works():
    return render_template('pages/howItWorks.html',page='how it works')


@app_views.route("/register")
def register():
    return render_template('pages/register.html',page='auth_page')

@app_views.route('/about')
def about_us():
    return render_template('pages/about_us.html')


