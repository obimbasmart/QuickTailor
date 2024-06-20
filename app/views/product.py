"""
cloud storage module
"""



from app.views import app_views
from flask import render_template, abort, redirect, url_for
from flask_login import current_user
from ..db_access.product import _get_products
from app import s3_client
from app.forms.main_forms import OrderMeasurementForm

@app_views.route('/products/<product_id>', methods=["GET"])
def get_product_by_id(product_id=None):
    if product_id is None:
        abort(404)

    product = _get_products(id=product_id)
    form = OrderMeasurementForm()
    print(product[0].reviews)
    return render_template('pages/product.html', form=form, product=product[0], page="products")

   

@app_views.route('/products', methods=["GET"])
def get_all_products():
    if not current_user.is_anonymous and current_user.is_tailor:
        return redirect(url_for('tailor_views.get_all_products'))
    
    products = _get_products(on_draft=False) 
    return render_template('pages/products.html',
                           page="products",
                           products=products)



