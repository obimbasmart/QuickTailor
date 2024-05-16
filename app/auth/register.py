#!/usr/bin/env python3


""" register route """
from app.auth import auth_views
from app.forms import RegistrationForm

from flask import request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from app.constants import USER_SIDEBAR_LINKS

@auth_views.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the registration data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        password = form.password.data
        # For demonstration purposes, I'll just print the data
        print(f'First Name: {first_name}, Last Name: {last_name}, Email: {email}, Phone Number: {phone_number}, Password: {password}')
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template('pages/register.html',
                           user_sidebar_links = USER_SIDEBAR_LINKS, form=form)

