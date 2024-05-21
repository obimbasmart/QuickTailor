
"""_summary_: handle /register and /login endpoints
"""

""" register route """
from app.auth import auth_views
from app.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.models.tailor import Tailor
from app import db
from flask import render_template, abort, flash, redirect, url_for
from app.constants import (USER_SIDEBAR_LINKS)

@auth_views.route("/register/<user_type>", methods=["GET", "POST"])
def register(user_type=None):

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
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return email
    return render_template('forms/login.html',
                        user_sidebar_links = USER_SIDEBAR_LINKS, 
                        form=form)