from app.views import app_views
from flask import render_template, request, jsonify, abort, redirect, flash
from flask_wtf.csrf import generate_csrf
from app.db_access.product import _get_products
from app.forms.main_forms import OrderMeasurementForm
from decimal import Decimal
from flask_login import current_user
from app.models.cart import CartItem
from app import db
from app.db_access.product import _get_product_with_img_urls
from app.forms.tailor_forms import CRSForm


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
            print(field_name, field)
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
        print("OKddd")
        cart_item = CartItem.query.filter_by(product_id=product_id, user_id=current_user.id).first()
        db.session.delete(cart_item)
        db.session.commit()
        return ""

@app_views.route('/cart')
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    products = [cart_item.product for cart_item in cart_items]
    products = _get_product_with_img_urls(products, no_images=1)
    form = CRSForm()
    return render_template('pages/cart.html', products=products, form=form)



# @app_views.route('/cart', methods=["GET", "POST"])
# def cart():

#     if request.method == "POST":
#         data = request.json
#         cart_items = data.get('cart_items')
#         if cart_items:
#         # Process the cart items and generate the response
#             _data = [{
#                 "image_url": url_for('static', filename='images/product_image_3.png'),
#                 "name": "Agbada Buba",
#                 "price": 10500,
#                 "total_price": 10500,
#                 "customization_value": 105000,
#                 "id": 1234
#                  },
#                  {
#                 "image_url": url_for('static', filename='images/product_image_3.png'),
#                 "name": "Agbada Lace",
#                 "price": 50500,
#                 "total_price": 10500,
#                 "id": 1234,
#                 "customization_value": 105000
#                  },
#                  {
#                 "image_url": url_for('static', filename='images/product_image_3.png'),
#                 "name": "Agbada Ankara",
#                 "price": 10500,
#                 "total_price": 10500,
#                 "id": 1234,
#                 "customization_value": 105000
#                  },
#                  {
#                 "image_url": url_for('static', filename='images/product_image_3.png'),
#                 "name": "Agbada Ankara",
#                 "price": 20500,
#                 "total_price": 100500,
#                 "id": 1234,
#                 "customization_value": 10000
#                  },
#                  {
#                 "image_url": url_for('static', filename='images/product_image_3.png'),
#                 "name": "Agbada Ankara",
#                 "price": 50000,
#                 "total_price": 140500,
#                 "id": 1234,
#                 "customization_value": 15000
#                  }

# ]
#             response_data = []
#             for cart_item_id in cart_items:
#                 for item in _data:
#                     if item['id'] == cart_item_id:
#                         response_data.append(item)
#                         break  
#             return jsonify(response_data), 200
#         return jsonify([]), 400
#     form =  CustomizationForm()
#     return render_template('pages/cart.html', data=notification, form=form)

# @app_views.route('/user/save', methods=["GET", "POST"])
# def save():
#     form =  CustomizationForm()
#     return render_template('pages/save.html', data=notification, form=form)



