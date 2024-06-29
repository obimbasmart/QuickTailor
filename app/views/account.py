from app.views import app_views
from flask import render_template, redirect,  url_for, flash
from flask_login import current_user
from app.forms.account import ResetEmailForm, ResetPasswordForm, UpdateAccountForm
from flask_login import login_required
from app.models.user import User
from email_service.sendgrid import send_otp
from app.models import db


@app_views.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form: UpdateAccountForm = UpdateAccountForm()

    form.first_name.default = current_user.first_name
    form.last_name.default = current_user.last_name
    form.phone_no.default = current_user.phone_no
    form.email.default = current_user.email

    if form.validate_on_submit():
        ignore_attrs = ['photo', 'submit', 'csrf_token', "email"]
        for field in form:
            if field.name not in ignore_attrs and field.data != getattr(current_user, field.name):
                setattr(current_user, field.name, field.data)

        db.session.commit()
        flash("Update successfull")
        return redirect(url_for('app_views.account'))
    
    return render_template('pages/account.html', form=form, current_user=current_user,
                           email_reset_form=ResetEmailForm(),
                           password_reset_form=ResetPasswordForm())

@app_views.route('/account/email', methods=["POST"])
def email():
    form = ResetEmailForm()

    try:
        form.validate_email(form.email)
    except:
        flash("Email already exist")
        return redirect(url_for('app_views.account'))
    
    if User.verify_otp(current_user.id, form.otp.data):
        if form.email.data != current_user.email:
            setattr(current_user, 'email', form.email.data)
            current_user.clear_reset_token()
            db.session.commit()
            flash("Update successfull")

    return redirect(url_for('app_views.account'))

@app_views.route('/account/password', methods=["POST"])
def password():
    form = ResetPasswordForm()
    if form.password.data != form.confirm_password.data:
        flash("Password does not match")

    elif User.verify_otp(current_user.id, form.otp.data):
        current_user.set_password(form.password.data)
        current_user.clear_reset_token()
        db.session.commit()
        flash("Update successfull")
        return redirect(url_for('auth_views.logout'))

    return redirect(url_for('app_views.account'))

@app_views.route('/account/user/code', methods=['POST'])
def _send_otp():
    otp = current_user.generate_otp()
    status_code = send_otp(current_user, otp)
    if status_code == 202:
        return """
                <div class='inline-flex gap-1 items-center justify-center'>
                            <span>Sent</span>   
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 84 84" fill="none">
                    <path opacity="0.5" d="M84 42C84 65.1958 65.1958 84 42 84C18.804 84 0 65.1958 0 42C0 18.804 18.804 0 42 0C65.1958 0 84 18.804 84 42Z" fill="#03CB2F" fill-opacity="0.15"/>
                    <path d="M58.9276 29.2727C60.1578 30.5028 60.1578 32.4973 58.9276 33.7273L37.9276 54.7273C36.6975 55.9575 34.7033 55.9575 33.473 54.7273L25.073 46.3273C23.8429 45.0972 23.8429 43.103 25.073 41.8728C26.3031 40.6426 28.2976 40.6426 29.5278 41.8728L35.7004 48.0451L45.0865 38.659L54.4731 29.2727C55.7033 28.0426 57.6975 28.0426 58.9276 29.2727Z" fill="#03CB2F"/>
                    </svg>
                </div>
            """
    return """
                <div class='inline-flex gap-1 items-center justify-center'>
                            <span>Error</span>   
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 85 84" fill="none">
                        <g clip-path="url(#clip0_6142_44180)">
                            <path opacity="0.5" d="M84 42C84 65.1958 65.1958 84 42 84C18.804 84 0 65.1958 0 42C0 18.804 18.804 0 42 0C65.1958 0 84 18.804 84 42Z" fill="#FF0000" fill-opacity="0.15"/>
                            <path d="M29 56L42.5001 42.5001M42.5001 42.5001L56 29M42.5001 42.5001L29 29M42.5001 42.5001L56 56" stroke="#FF0000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
                        </g>
                        <defs>
                            <clipPath id="clip0_6142_44180">
                            <rect width="84" height="84" fill="white" transform="translate(0.5)"/>
                            </clipPath>
                        </defs>
                        </svg>
                </div>
            """
