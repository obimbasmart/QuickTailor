
"""_summary_: handle /register and /login endpoints
"""

""" register route """


from app.auth import auth_views
from app.forms.auth_forms import RegistrationForm, LoginForm
from app.models.user import User
from app.models.tailor import Tailor
from app.models import db
from flask import render_template, abort, flash, redirect, request, url_for
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user
from app.constants import (USER_SIDEBAR_LINKS)
from email_service.sendgrid import send_email_verification
from app.models.temp import AnonymousUserRecord
from app.models.base_user import BaseUser

@auth_views.route('/verify_email/<token>', methods=["GET"])
def activate_account(token=None):
    not_registered_user = AnonymousUserRecord.query.filter_by(id=token).one_or_none()
    msg = "The link is expired or invalid"

    if not_registered_user:
        if not_registered_user.data['user_type'] == "user":
                new_user = User(first_name=not_registered_user.data['first_name'],
                                last_name=not_registered_user.data['last_name'],
                                email=not_registered_user.data['email'],
                                phone_no=not_registered_user.data['phone_no'])
        else:
            new_user = User(first_name=not_registered_user.data['first_name'],
                                last_name=not_registered_user.data['last_name'],
                                email=not_registered_user.data['email'],
                                phone_no=not_registered_user.data['phone_no'])
            
        msg = "Email verification successfull!"

        new_user.set_password(not_registered_user.data['password'])
        db.session.add(new_user)
        db.session.delete(not_registered_user)
        db.session.commit()
        
    flash(msg)
    return redirect(url_for('auth_views.login'))


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

        full_name = form.full_name.data.split()
        first_name = full_name[0]
        try:
            last_name = full_name[1]
        except IndexError:
            last_name = None


        not_registered_user = AnonymousUserRecord(
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': form.email.data,
                'password': form.password.data,
                'phone_no': form.phone_number.data,
                'user_type': user_type
            }
        )

        status = send_email_verification(first_name, form.email.data, not_registered_user.id)
        print("EmailStatus: ", status)
        db.session.add(not_registered_user)
        db.session.commit()
        flash("Verify your email to continue")
        return redirect(url_for('auth_views.login'))

    return render_template('forms/register_user.html',
                           user_sidebar_links=USER_SIDEBAR_LINKS,
                           form=form)


@auth_views.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(request.referrer or url_for('app_views.home'))
    
    is_anonymouse = form.email.data in [user.data['email'] for user in AnonymousUserRecord.query.all()]
    
    if is_anonymouse:
        flash("Verify your email to continue")
        return redirect(url_for('auth_views.login'))

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
                           user_sidebar_links=USER_SIDEBAR_LINKS,
                           form=form, page="auth_page")


@auth_views.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Logout successfull")
    return redirect(url_for('app_views.home'))
