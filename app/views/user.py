

from flask import render_template, redirect, url_for
from app.views import app_views
from app.forms.main_forms import MeasurementForm
from app.models.tailor import Tailor
from app.db_access.product import _get_product_with_img_urls
from app import s3_client

@app_views.route('/<brand_name>')
def tailor_profile(brand_name=None):
    if brand_name is None:
        return redirect(url_for('app_views.home'))

    tailor = Tailor.query.filter_by(business_name=brand_name).one_or_404()
    products = _get_product_with_img_urls(tailor.products, no_images=1)
    reviews = [
        review for product in tailor.products
        for review in product.reviews
    ]
    return render_template('pages/tailor_profile.html', reviews=reviews,
                           products=products, tailor=tailor)