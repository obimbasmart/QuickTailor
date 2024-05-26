from app.views import app_views
from flask import render_template, request, jsonify, url_for
from app.constants import USER_SIDEBAR_LINKS
from cloud_storage.s3_cloud_storage import S3StorageService
from app.views.index import notification
from app.forms.cart_forms import CustomizationForm
# endpoint tto generate csrf token
from flask_wtf.csrf import generate_csrf

@app_views.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    return jsonify({'csrf_token': token})

@app_views.route('/user/cart', methods=["GET", "POST"])
def cart():

    if request.method == "POST":
        data = request.json
        cart_items = data.get('cart_items')
        if cart_items:
        # Process the cart items and generate the response
            _data = [{
                "image_url": url_for('static', filename='images/product_image_3.png'),
                "name": "Agbada Buba",
                "price": 10500,
                "total_price": 10500,
                "customization_value": 105000,
                "id": 1234
                 },
                 {
                "image_url": url_for('static', filename='images/product_image_3.png'),
                "name": "Agbada Lace",
                "price": 50500,
                "total_price": 10500,
                "id": 1234,
                "customization_value": 105000
                 },
                 {
                "image_url": url_for('static', filename='images/product_image_3.png'),
                "name": "Agbada Ankara",
                "price": 10500,
                "total_price": 10500,
                "id": 1234,
                "customization_value": 105000
                 },
                 {
                "image_url": url_for('static', filename='images/product_image_3.png'),
                "name": "Agbada Ankara",
                "price": 20500,
                "total_price": 100500,
                "id": 1234,
                "customization_value": 10000
                 },
                 {
                "image_url": url_for('static', filename='images/product_image_3.png'),
                "name": "Agbada Ankara",
                "price": 50000,
                "total_price": 140500,
                "id": 1234,
                "customization_value": 15000
                 }

]
            response_data = []
            for cart_item_id in cart_items:
                for item in _data:
                    if item['id'] == cart_item_id:
                        response_data.append(item)
                        break  
            return jsonify(response_data), 200
        return jsonify([]), 400
    form =  CustomizationForm()
    return render_template('pages/cart.html', data=notification, form=form)

@app_views.route('/user/save', methods=["GET", "POST"])
def save():
    form =  CustomizationForm()
    return render_template('pages/save.html', data=notification, form=form)



