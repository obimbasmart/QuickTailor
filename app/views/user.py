

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
    tailor.img_url = s3_client.generate_presigned_url('get_object', tailor.photo_url)
    products = _get_product_with_img_urls(tailor.products, no_images=1)
    return render_template('pages/tailor_profile.html', tailor=tailor, products=products)


@app_views.route('/measurement', methods=["GET", "POST"])
def get_set_measurement():
    form = MeasurementForm()
    if form.validate_on_submit():
        return "Submitted"
    return render_template('pages/measurements.html',
                           form=form)
