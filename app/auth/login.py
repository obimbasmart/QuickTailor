#!/usr/bin/env python3

""" login route """
from app.auth import auth_views
from app.forms import LoginForm
from flask import (request, render_template, redirect, url_for, flash)
from app.constants import (USER_SIDEBAR_VISITORS, Login_fields, auth_top)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length


@auth_views.route("/login", methods=["GET", "POST"])
def login():
    """ Route for login, both users and tailors """
    form = LoginForm()
    field_methods = {
    "email": form.email,
    "password": form.password,
    "submit" : form.submit,
    "hidden": form.hidden_tag()

    }
    if form.validate_on_submit():
     # Process the registration data
        email = form.email.data
        password = form.password.data


    if request.method == "GET":
        return render_template('pages/login.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS, 
                           top_div = auth_top['login'], 
                           forms_field=Login_fields, submit="Login", form=field_methods)
    return "HELLO"

