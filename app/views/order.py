
"""
Index
"""


from flask_login import current_user
from flask import render_template, abort, redirect, url_for, request
from app.views import app_views
from app.db_access.product import _get_products
from app.models.order import Order
from app.forms.main_forms import OrderMeasurementForm
from decimal import Decimal
from app.db_access.product import _get_product_with_img_urls
from app.models.cart import CartItem


@app_views.route("/cart/checkout")
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    for cart_item in cart_items:
        cart_item.product.customization_value = cart_item.cusomization_value
    products = [cart_item.product for cart_item in cart_items]

    for product in products:
        print(product.customization_value)
    
    products = _get_product_with_img_urls(products, no_images=1)
    return render_template('pages/checkout.html', products=products)



@app_views.route("/products/<product_id>/order", methods=["POST"])
def order(product_id=None):

    form = OrderMeasurementForm()
    if form.validate_on_submit():
        measurements = {}
        for field_name, field in form.data.items():
            print(field_name, field)
            if isinstance(field, Decimal):
                measurements[field_name] = float(field)
            current_user.measurements = measurements

    product = _get_products(id=product_id)[0]
    if not product:
        abort(404)

    order = Order(product_id=product.id, user_id=current_user.id)
    order.measurements = measurements
    return redirect(request.referrer)



#