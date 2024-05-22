#!/usr/bin/env python3


""" register route """
from app.auth import auth_views
from app.forms import RegistrationForm
from app.models.user import User
from app.models.tailor import Tailor
from app import db
from flask import request, render_template, abort, flash, redirect, url_for
from app.constants import (USER_SIDEBAR_VISITORS, USER_SIDEBAR_LINKS, 
                           Create_user_fields,
        Tailor_address_fields,
        Tailor_verification_fields, auth_top, Registration_page_options)


@auth_views.route("/register/tailor/address", methods=["GET", "POST"])
def register_tailor_address():
    """ Route for tailor address verification """
    form = RegistrationForm()
    field_methods = {
    "street": form.street,
    "city": form.city,
    "state": form.state,
    "submit" : form.submit,
    "hidden": form.hidden_tag()

    }

    if form.validate_on_submit():
     # Process the registration data
        street = form.street.data
        city = form.city.data
        state = form.state.data

    if request.method == "GET":
        return render_template('pages/tailor_address.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS,
                           top_div = auth_top['tailor_address'],
                           forms_field=Tailor_address_fields, 
                           submit=["Skip", "Next", "/register/tailor/verification"], form=field_methods)
    return "HELLO"
@auth_views.route("/register/tailor/verification", methods=["GET", "POST"])
def register_tailor_verification():
    """ Route for tailor verification of NIN, and uploads of relevant
    documents
    """
    form = RegistrationForm()
    field_methods = {
    "nin": form.nin,
    "upload_nin_slip": form.nin_slip,
    "upload_your_photo": form.your_photo,
    "submit" : form.submit,
    "hidden": form.hidden_tag()

    }

    if form.validate_on_submit():
     # Process the registration data
        nin = form.nin.data
        nin_slip  = form.nin_slip.data
        your_photo = form.your_photo.data

    if request.method == "GET":
        return render_template('pages/tailor_verification.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS,
                           top_div = auth_top['tailor_verification'],
                           forms_field=Tailor_verification_fields,
                           submit=["Skip", "Verify", "/register/tailor/brand"],form=field_methods )
    return "HELLO"

