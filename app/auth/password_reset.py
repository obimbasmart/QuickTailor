#!/usr/bin/env python3

""" Password reset routes """
from app.auth import auth_views
from app.forms import ResetForm,  ResetPasswordForm
from app.models.user  import User
from app.models.tailor import Tailor
from flask import (request, render_template, flash,  redirect, url_for)
from app.constants import (USER_SIDEBAR_VISITORS, Password_reset_fields,
        auth_top, Reset_fields)
from app.config import Config
from app import db
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

@auth_views.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    """ first route for reseting password """

    form = ResetForm()
    if form.validate_on_submit():
    # Process the registration data
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        tailor = Tailor.query.filter_by(email=email).first()

        # to avoid excess if statement, switch user to tailor if user is None since it's one mail per user
        if tailor:
            user = tailor
        token = serializer.dumps(user.email, salt='password-reset-salt')
        user.generate_reset_token(token)
        reset_link = url_for('auth_views.set_new_password', token = token, _external=True)
        # Send reset link using email service
        flash("reset link has been sent to you")
        return reset_link

    return render_template('forms/password_reset.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS,
                           form=form)

@auth_views.route("/set_new_password/<token>", methods=["GET", "POST"])
def set_new_password(token):
    """ Route for setting new password after submitting email
    """

    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)
    except:
       flash("The reset link is invalid or has expired.")
       return redirect(url_for('auth_views.password_reset'))
    print(email)
    user = User.query.filter_by(email=email).first()
    tailor = Tailor.query.filter_by(email=email).first()
    # to avoid excess if statement, switch user to tailor if user is None since it's one mail per user
    if tailor:
        user = tailor

    # Ensure user exists and token matches the stored reset token
    if  user.reset_token != token:
        print(user.reset_token, token)
        flash("The reset link is invalid or has expired.")
        return redirect(url_for('auth_views.password_reset'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
    # Process the registration data
        user.set_password(form.password.data)
        db.session.commit()
        user.clear_reset_token()
        flash('Password change successful')
        print(user)
        return redirect(url_for("auth_views.login"))

    return render_template('forms/reset_password_page.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS,
                           form=form)


