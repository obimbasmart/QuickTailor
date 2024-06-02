
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