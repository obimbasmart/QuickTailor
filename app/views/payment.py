from app.views import app_views
from flask import render_template, request
from app.constants import USER_SIDEBAR_LINKS
# from cloud_storage.s3_cloud_storage import S3StorageService
from app.forms.cart_forms import CustomizationForm


@app_views.route('/payment', methods=["GET", "POST"])
def payment():
    form =  CustomizationForm()
    return render_template('pages/payment.html', form=form)


