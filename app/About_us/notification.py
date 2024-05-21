#!/usr/bin/env python3

import os
from flask import render_template
from app.About_us import page_viewer


@page_viewer.route('/notifications')
def user_notication():
    return render_template('pages/notification.html')

#More function to handle user notification based on order progress
