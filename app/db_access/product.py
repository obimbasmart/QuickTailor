
"""_summary_

    This module encapsulates frequent request to the database
    The reason for having a seperate DB_ACCESS folder is to enhance
    request by implementing Caching
"""

from app.models.product import Product
from app import s3_client


def _get_products(no_images: int =4, **filters):
     result = Product.query.filter_by(**filters).all()
     return _get_product_with_img_urls(result, no_images)

def _get_product_with_img_urls(product_list: list, no_images: int):
    for product in product_list:
        product.img_urls = s3_client.generate_presigned_urls(
            'get_object', list(product.images.values())[:no_images])
    return product_list
