#!/usr/bin/env python3

""" Password reset routes """
from app.auth import auth_views
from app.forms import ResetForm,  ResetPasswordForm
from app.models.user  import User
from app.models.tailor import Tailor
from flask import (render_template, flash,  redirect, url_for)
from app.constants import (USER_SIDEBAR_VISITORS)
from app import db
from flask_login import current_user
from app.models.base_user import BaseUser
from email_service.sendgrid import send_password_reset_email


@auth_views.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    """ first route for reseting password """
    form = ResetForm()
    if form.validate_on_submit():

        email = form.email.data
        normal_user = User.query.filter_by(email=email).first()
        tailor = Tailor.query.filter_by(email=email).first()

        user = normal_user or tailor
        response = send_password_reset_email(user)
        flash("reset link has been sent to you")

    return render_template('forms/password_reset.html',
                           form=form, page='auth_page')

@auth_views.route("/set_new_password/<token>", methods=["GET", "POST"])
def set_new_password(token):
    """ Route for setting new password after submitting email
    """
    if current_user.is_authenticated:
        return redirect(url_for('app_views.home'))
    
    user = BaseUser.verify_reset_password_token(token)
    
    if user is None or user.reset_token != token:
       flash("The reset link is invalid or has expired.")
       return redirect(url_for('auth_views.password_reset'), page='auth_page')
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        user.clear_reset_token()
        flash('Password reset successfull')
        return redirect(url_for("auth_views.login"))

    return render_template('forms/reset_password_page.html',
                           form=form, page='auth_page')


