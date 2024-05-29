
"""_summary_

    This module encapsulates frequent request to the database
    The reason for having a seperate DB_ACCESS folder is to enhance
    request by implementing Caching
"""

from app.models.product import Product
from app import s3_client

def _get_all_products():
    products = Product.query.all()
    for product in products:
        img_urls = s3_client.generate_presigned_urls('get_object', product.images.values())
        product.img_urls = img_urls
    return products

def _get_product(product_id):
    product = Product.query.filter_by(id=product_id).one_or_404()
    product.img_urls = s3_client.generate_presigned_urls('get_object', product.images.values())
    return product
