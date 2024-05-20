#!/usr/bin/env python3

""" Password reset routes """
from app.auth import auth_views
from app.forms import LoginForm
from flask import (request, render_template, redirect, url_for, flash)
from app.constants import (USER_SIDEBAR_VISITORS, Password_reset_fields,
        auth_top, Reset_fields)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length


@auth_views.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    """ first route for reseting password """
    form = LoginForm()
    field_methods = {
    "email": form.email,
    "submit" : form.submit,
    "hidden": form.hidden_tag()

    }

    if form.validate_on_submit():
    # Process the registration data
        email = form.email.data

    if request.method == "GET":
        return render_template('forms/password_reset.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS,
                           top_div = auth_top['password_reset'], 
                           forms_field=Password_reset_fields, 
                           submit="Reset Password", form=field_methods)
    return redirect(url_for('auth_views.set_new_password'))

@auth_views.route("/set_new_password", methods=["GET", "POST"])
def set_new_password():
    """ Route for setting new password after submitting email
    """

    form = LoginForm()
    field_methods = {
    "password": form.password,
    "confirm_password": form.confirm_password,
    "submit" : form.submit,
    "hidden": form.hidden_tag()

    }
    if form.validate_on_submit():
     # Process the registration data
        password = form.password.data

    if request.method == "GET":
        return render_template('pages/reset_password_page.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS,
                           top_div = auth_top['reset'],
                           forms_field=Reset_fields,
                           submit="Reset Password", form=field_methods)
    return redirect(url_for('auth_views.password_reset'))


