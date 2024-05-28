
from flask import render_template, redirect, url_for, request
from app.tailor import tailor_views
from app.auth.decorators import tailor_required
from app.forms.tailor_forms import CreateProductForm
from app.models.product import Product
from flask_login import current_user
from app import db, s3_client
from app.forms.tailor_forms import CRSForm

@tailor_views.route('/my_products/new', methods=["GET", "POST"])
@tailor_required
def create_product():
    form = CreateProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name = form.name.data, description=form.description.data,
            price = float(form.price.data), estimated_tc=form.estimated_tc.data,
            material = form.material.data, tailor_id=current_user.id,
            categories=form.categories.data + form.gender.data
        )
        
        img_urls = s3_client.upload_files(form.images.data, new_product.tailor_id, new_product.id)
        new_product.images = img_urls
        db.session.add(new_product)
        db.session.commit()
        return  redirect(url_for('tailor_views.get_all_products'))
    return render_template('forms/tailor_forms/create_product.html', form=form)


@tailor_views.route("/my_products")
@tailor_required
def get_all_products():
    products = Product.query.filter_by(tailor_id=current_user.id).all()
    for product in products:
        img_url = s3_client.generate_presigned_url('get_object', product.images['img_0'])
        product.img_url = img_url
    form = CRSForm()
    return render_template('pages/tailor/products.html',
                           page='my products', products=products, form=form)


@tailor_views.route('/delete_product', methods=['DELETE'])
def delete_product():
    id = request.form.get('id')
    product = Product.query.get_or_404(id)
    print(product.images)
    s3_client.delete_files(product.images.values())
    db.session.delete(product)
    db.session.commit()
    return render_template('partials/delete_successfull.html')
    