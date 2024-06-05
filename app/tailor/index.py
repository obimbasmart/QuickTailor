
"""
Index
"""


from flask import render_template, flash, request
from app.tailor import tailor_views
from app.auth.decorators import tailor_required
from app.forms.tailor_forms import BrandInformationForm
from flask_login import current_user
from app import db, s3_client
from app.models.order import Order


@tailor_views.route("/dashboard")
@tailor_required
def dashboard():
    products = [product.id for product in current_user.products]
    orders = Order.query.all()
    my_orders = [
        order for order in orders
        if order.product_id in products
    ]
    return render_template('pages/tailor/dashboard.html',
                           page='dashboard', orders=my_orders)


@tailor_views.route("/dashboard")
@tailor_required
def profile():
    return render_template('pages/home.html',
                           page='dashboard')


@tailor_views.route("/account")
@tailor_required
def account():
    return render_template('pages/tailor/account.html',
                           page='account')


@tailor_views.route('/my_brand', methods=['GET', 'POST'])
@tailor_required
def my_brand():
    form = BrandInformationForm()
    if form.validate_on_submit():
        ignore_attrs = ['photo', 'submit', 'csrf_token']
        for field in form:
            if field.name not in ignore_attrs and field.data != getattr(current_user, field.name):
                setattr(current_user, field.name, field.data)

        if form.photo.data:
            img_url = s3_client.upload_profile_photo(
                form.photo.data, current_user.id)
            current_user.photo_url = img_url

        db.session.commit()
        flash("Update successfull")
    return render_template('forms/tailor_forms/brand_information.html', form=form)
