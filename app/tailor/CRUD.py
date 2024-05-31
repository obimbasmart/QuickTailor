
from flask import render_template, redirect, url_for, request, abort, flash
from app.tailor import tailor_views
from app.auth.decorators import tailor_required
from app.forms.tailor_forms import CreateProductForm
from app.models.product import Product
from flask_login import current_user
from app import db, s3_client
from app.forms.tailor_forms import CRSForm
from app.db_access.product import _get_products


@tailor_views.route('/my_products/new', methods=["GET", "POST"])
@tailor_required
def create_product():
    form = CreateProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data, description=form.description.data,
            price=float(form.price.data), estimated_tc=form.estimated_tc.data,
            material=form.material.data, tailor_id=current_user.id,
            categories=form.categories.data + form.gender.data, on_draft=form.draft.data
        )

        img_urls = s3_client.upload_files(
            form.images.data, new_product.tailor_id, new_product.id)
        new_product.images = img_urls
        db.session.add(new_product)
        db.session.commit()
        flash("Product successfully added to your store!")
        return redirect(url_for('tailor_views.get_all_products'))
    return render_template('forms/tailor_forms/create_product.html', form=form)


@tailor_views.route("/my_products")
@tailor_required
def get_all_products():
    products = _get_products(tailor_id=current_user.id, no_images=1)
    form = CRSForm()
    return render_template('pages/tailor/products.html',
                           page='my products', products=products, form=form)


@tailor_views.route('/products', methods=['POST'])
@tailor_required
def update_product_visibility():
    _id = request.form.get('id')
    action = request.form.get('action')

    if not action and _id:
        abort(400)
    if action not in ['to_draft', 'from_draft', 'delete']:
        abort(400)

    product = Product.query.get_or_404(_id)
    msg = "Product successfully deleted from your store!"
    if action == 'delete':
        product = Product.query.get_or_404(_id)
        s3_client.delete_files(product.images.values())
        db.session.delete(product)
    elif action == "from_draft":
        product.on_draft = False
        msg = "Success! Your product is now live!"
    else:
        product.on_draft = True
        msg = "Success! Your product is now inactive!"
    db.session.commit()
    flash(msg)
    return redirect(url_for('tailor_views.get_all_products'))
