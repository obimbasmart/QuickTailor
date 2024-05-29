
"""
Index
"""


from flask import render_template, flash
from app.tailor import tailor_views
from app.auth.decorators import tailor_required
from app.forms.tailor_forms import BrandInformationForm
from flask_login import current_user
from app import db, s3_client

@tailor_views.route("/dashboard")
@tailor_required
def dashboard():
    return render_template('pages/home.html',
                           page='dashboard')


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
        if form.brand_name.data != current_user.business_name:
            current_user.business_name = form.brand_name.data

        if form.cac_number.data != current_user.cac_number:
            current_user.cac_number = form.cac_number.data

        if form.about.data != current_user.about:
            current_user.about = form.about.data

        if form.bank_name.data != current_user.bank_name:
            current_user.bank_name = form.bank_name.data

        if form.account_name.data != current_user.account_name:
            current_user.account_name = form.account_name.data

        if form.account_number.data != current_user.account_number:
            current_user.account_number = form.account_number.data

        if form.photo.data:
            # photo_url = s3_client.upload_profile_photo(form.photo, current_user.id)
            # print(photo_url)
            print(form.photo.data)

        
            
        db.session.commit()
        flash("Update successfull")
    return render_template('forms/tailor_forms/brand_information.html', form=form)