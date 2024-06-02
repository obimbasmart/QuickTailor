"""
Testing cloud storage module
"""



from app.views import app_views
from flask import render_template, abort
from app.db_access.product import _get_product, _get_all_products

@app_views.route('/products/<product_id>', methods=["GET"])
def get_product_by_id(product_id=None):
    if product_id is None:
        abort(404)
    product = _get_product(product_id)
    return render_template('pages/product.html', product=product, page="products")

   

@app_views.route('/products', methods=["GET", "POST"])
def get_all_products():
    products = _get_all_products()
    print(products)
    return render_template('pages/products.html',
                           page="products",
                           products=products)



