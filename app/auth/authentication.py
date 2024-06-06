
"""_summary_: handle /register and /login endpoints
"""

""" register route """
from app.auth import auth_views
from app.forms.auth_forms import RegistrationForm, LoginForm
from app.models.user import User
from app.models.tailor import Tailor
from app import db
from flask import render_template, abort, flash, redirect, request, url_for
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user
from app.constants import (USER_SIDEBAR_LINKS)

@auth_views.route("/register/<user_type>", methods=["GET", "POST"])
def register(user_type=None):
    if current_user.is_authenticated:
        return redirect(url_for('app_views.home'))

    if user_type is None:
        return render_template('pages/register.html')
    
    if user_type not in ['user', 'tailor']:
        abort(404)

    form = RegistrationForm()
    if form.validate_on_submit():
        if user_type == "user":
            new_user = User(first_name=form.first_name.data,
                            last_name="good name",
                            email=form.email.data,
                            phone_no=form.phone_number.data)
        else:
            new_user = Tailor(first_name=form.first_name.data,
                              last_name="good name",
                              email=form.email.data,
                              phone_no=form.phone_number.data)
    
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successfull")
        return redirect(url_for('auth_views.login'))
    return render_template('forms/register_user.html',
                        user_sidebar_links = USER_SIDEBAR_LINKS,
                        form=form)


@auth_views.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(request.referrer or url_for('app_views.home'))
    
    if form.validate_on_submit():
        normal_user = User.query.filter_by(email=form.email.data).one_or_none()
        tailor = Tailor.query.filter_by(email=form.email.data).one_or_none()

        user = normal_user or tailor

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', "error")
            return redirect(url_for('auth_views.login'))

        login_user(user, remember=form.remember_me.data)

        # redirect to the url that led to the login page
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("app_views.home")
        flash('Login successfull')
        return redirect(next_page)
        
    return render_template('forms/login.html',
                        user_sidebar_links = USER_SIDEBAR_LINKS, 
                        form=form, page="auth_page")

@auth_views.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Logout successfull")
    return redirect(url_for('app_views.home'))
