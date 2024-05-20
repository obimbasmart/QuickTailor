#!/usr/bin/env python3


""" register route """
from app.auth import auth_views
from app.forms import RegistrationForm

from flask import request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from app.constants import (USER_SIDEBAR_VISITORS, Create_user_fields,
        Create_tailor_fields, Tailor_address_fields,
        Tailor_verification_fields, auth_top, Registration_page_options)

@auth_views.route("/register/user", methods=["GET", "POST"])
def register_user():

    """ Route for user registeation """
    form = RegistrationForm()
    field_methods = {
    "name": form.name,
    "email": form.email,
    "phone_number": form.phone_number,
    "password": form.password,
    "submit" : form.submit,
    "hidden": form.hidden_tag()
    
}
    if form.validate_on_submit():
     # Process the registration data
        email = form.email.data
        phone_number = form.phone_number.data
        password = form.password.data
        name = form.name.data
     
    if request.method == "GET":
        return render_template('forms/register_user.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS,
                           top_div = auth_top['create_user'],
                           forms_field=Create_user_fields, submit="Create my account", form=field_methods)
    return "HELLO"
@auth_views.route("/register/tailor", methods=["GET", "POST"])
def register_tailor():
    """ Route for tailor registration """
    form = RegistrationForm()
    field_methods = {
    "name": form.name,
    "email": form.email,
    "phone_number": form.phone_number,
    "password": form.password,
    "submit" : form.submit,
    "hidden": form.hidden_tag()

    }
  
    if form.validate_on_submit():
     # Process the registration data
        email = form.email.data
        phone_number = form.phone_number.data
        password = form.password.data
        name = form.name.data


    if request.method == "GET":
        return render_template('forms/register_user.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS,
                           top_div = auth_top['create_tailor'],
                           forms_field=Create_user_fields, submit="Create my account", form=field_methods)
    return "HELLO"
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



@auth_views.route("/register", methods=["GET", "POST"])
def register():
    """ This is the route for registration selectio where user can select 
    either to register as tailor or normal user
    """
    form = RegistrationForm()
    field_methods = {
    "submit" : form.submit,
    "input_field": form.hidden,
    "hidden": form.hidden_tag()

    }


    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the user choice of registration
        option = form.submi.data
        
        # For demonstration purposes, I'll just print the data
        """flash('Registration successful!', 'success')"""
        return option
    if request.method == "GET":
        return render_template('forms/register.html', 
                            user_sidebar_links = USER_SIDEBAR_VISITORS,
                            top_div = ['Join Us today'], options =Registration_page_options,
                            submit = "Create account", form=field_methods)
    return "hello"
