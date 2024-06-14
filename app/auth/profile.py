#!/usr/bin/env python3
"Profile Page Route"

from app.auth import auth_views
from app.forms.auth_forms import RegistrationForm
from app.models.user import User
from app.models.tailor import Tailor
from app.models import db
from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask import jsonify


@auth_views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = RegistrationForm()

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            current_user.first_name = data.get(
                'first_name', current_user.first_name)
            current_user.email = data.get('email', current_user.email)
            if hasattr(current_user, 'phone_number'):
                current_user.phone_number = data.get(
                    'phone_number', current_user.phone_number)
            db.session.commit()
            return jsonify({'message': 'Profile updated successfully!'}), 200

        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.email = form.email.data
            if hasattr(current_user, 'phone_number'):
                current_user.phone_number = form.phone_number.data
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth_views.profile'))

    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.email.data = current_user.email
        if hasattr(current_user, 'phone_number'):
            form.phone_number.data = current_user.phone_number

    phone_number_exists = hasattr(current_user, 'phone_number')
    return render_template('forms/profile.html', form=form, phone_number_exists=phone_number_exists)
