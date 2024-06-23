from app.views import app_views
from flask import render_template, request, jsonify, abort, redirect, flash, url_for
from flask_wtf.csrf import generate_csrf
from app.db_access.product import _get_products
from app.forms.main_forms import OrderMeasurementForm
from decimal import Decimal
from flask_login import current_user
from app.models.cart import CartItem
from app.models import db
from app.db_access.product import _get_product_with_img_urls
from app.forms.tailor_forms import CRSForm
from app.forms.cart_forms import ApplyCodeForm
from app.models.tailor import Tailor
from app.models.product import Product


@app_views.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    return jsonify({'csrf_token': token})


@app_views.route('/products/<product_id>/cart', methods=["POST"])
def cart(product_id=None):
    form = OrderMeasurementForm()
    if form.validate_on_submit():
        measurements = {}
        for field_name, field in form.data.items():
            if isinstance(field, Decimal):
                measurements[field_name] = float(field)
            current_user.measurements = measurements

        product = _get_products(id=product_id)[0]
        if not product:
            abort(404)

        cart_item = CartItem(product_id=product.id, user_id=current_user.id)
        cart_item.measurements = measurements
        db.session.add(cart_item)
        db.session.commit()
        flash("Item added to cart")
        return redirect(request.referrer)
    return render_template('pages/cart.html')


@app_views.route('/products/<product_id>/cart', methods=["DELETE"])
def delete_from_cart(product_id=None):
    cart_item = CartItem.query.filter_by(
        product_id=product_id, user_id=current_user.id).first()
    db.session.delete(cart_item)
    db.session.commit()
    return ""


@app_views.route('/cart')
def view_cart():
    form = ApplyCodeForm()
    if current_user.is_anonymous:
        return redirect(url_for('auth_views.login'))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    for cart_item in cart_items:
        cart_item.product.customization_value = cart_item.cusomization_value
    products = [cart_item.product for cart_item in cart_items]

    for product in products:
        print(product.customization_value)

    products = _get_product_with_img_urls(products, no_images=1)
    return render_template('pages/cart.html', products=products, form=form)


@app_views.route('/cart/code', methods=["POST"])
def apply_code(user_id=None):
    form = ApplyCodeForm()
    if form.validate_on_submit():
        code = form.code.data
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

        for item in cart_items:
            if item.product.customization_tokens.get('all'):
                checkout_code = item.product.customization_tokens.get('all')
                code_details = Tailor.decode_customization_code(checkout_code)
                if code_details.get('value'):
                    CartItem.query.filter_by(id=item.id).one_or_404(
                    ).cusomization_value = code_details.get('value')
                    # db.session.add(item)
                    db.session.commit()
        return redirect(url_for('app_views.view_cart'))


@app_views.route('/me/saved', methods=["GET", "POST"])
def saved():
    if current_user.is_anonymous:
        products = []
    else:
        products = db.session.query(Product).filter(
            Product.id.in_(current_user.saved_items)).all()
    return render_template('pages/save.html', products=products)


@app_views.route('/product/<product_id>/save', methods=["POST"])
def save_item(product_id=None):

    if current_user.is_anonymous:
        return 'Not signed In'  # localStorage will do the work

    product = Product.query.filter_by(id=product_id).one_or_404()
    saved_items = current_user.saved_items
    print(current_user.saved_items)
    if saved_items:
        if not product_id in saved_items:
            current_user.saved_items.append(product_id)
        else:
            current_user.saved_items.remove(product_id)
    else:
        current_user.saved_items = [product_id]

    print(current_user.saved_items)
    db.session.commit()
    return "Success"
