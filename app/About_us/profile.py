#!/usr/bin/env python3

import os
from flask import render_template
from app.About_us import page_viewer


@page_viewer.route('/profile')
def user_profile():
    return render_template('forms/profile.html')