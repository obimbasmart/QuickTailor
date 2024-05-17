"""
Testing cloud storage module
"""



from app.views import app_views
from flask import render_template, request
from app.constants import USER_SIDEBAR_LINKS
from app.forms import CreateProductForm
from cloud_storage.s3_cloud_storage import S3StorageService


@app_views.route('/products', methods=["GET", "POST"])
def get_all_products():
    return render_template('pages/products.html',
                           user_sidebar_links=USER_SIDEBAR_LINKS, page="products")

@app_views.route('/products/1234', methods=["GET", "POST"])
def get_product_by_id():
    return render_template('pages/product.html',
                           user_sidebar_links=USER_SIDEBAR_LINKS, page="products")


@app_views.route('/products/upload', methods=["GET", "POST"])
def upload_product():
    form = CreateProductForm()
    if request.method == "POST":
        file = request.files.get('file')
        storage = S3StorageService('quicktailor-products-bucket')
        img_key = storage.upload_file(file, '444', '111')
        img_url = storage.generate_presigned_url('get_object', img_key)
        return f"<h1>Done. Url is <a href='{img_url}'>imgLink</a></h1>"
    return render_template('forms/create_product.html',
                           user_sidebar_links=USER_SIDEBAR_LINKS, form=form)

@app_views.route("/products/delete")
def delete_product():
    storage = S3StorageService('quicktailor-products-bucket')
    storage.delete_file('tailor-444/product-111/4c5bff6719734acb83c9108cfeb0dac3')
    return "<h1>Done</h1>"


