
"""
Index
"""


from flask_login import current_user, login_required
from flask import render_template, abort, redirect, url_for
from app.views import app_views
from app.models.order import Order
from app.db_access.product import _get_product_with_img_urls
from app.models.cart import CartItem
from app.models import db
from app.forms.main_forms import OrderMeasurementForm


@app_views.route('/orders/<order_id>')
@login_required
def view_order(order_id=None):
    form = OrderMeasurementForm()
    order = Order.query.filter_by(id=order_id).one_or_404()
    return render_template('pages/order.html', order=order, form=form)


@app_views.route('/orders')
@login_required
def orders():
    if not current_user.is_anonymous and current_user.is_tailor:
        products = [product.id for product in current_user.products]
        orders = Order.query.all()
        my_orders = [
            order for order in orders
            if order.product_id in products
        ]
        return render_template('pages/tailor/orders.html',
                               page='orders', orders=my_orders)
    orders = Order.query.filter_by(user_id=current_user.id)
    return render_template('pages/orders.html', page='order', orders=orders)


@app_views.route("/cart/checkout")
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    for cart_item in cart_items:
        cart_item.product.customization_value = cart_item.cusomization_value
    products = [cart_item.product for cart_item in cart_items]

    for product in products:
        print(product.customization_value)

    products = _get_product_with_img_urls(products, no_images=1)
    return render_template('pages/checkout.html', products=products)


@app_views.route("/cart/checkout/order", methods=["GET"])
@login_required
def order(product_id=None):
    cart = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart:
        abort(404)

    with db.session.no_autoflush:
        db.session.add_all([
            Order(product_id=item.product_id, user_id=current_user.id,
                  measurements=item.measurements)
            for item in cart
        ])

    # clear all items on cart
    [db.session.delete(item) for item in cart]

    db.session.commit()
    return render_template('pages/afterCheckout.html')
