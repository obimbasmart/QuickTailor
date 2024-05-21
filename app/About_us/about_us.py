#!/usr/bin/env python3

import os
from flask import render_template
from app.About_us import page_viewer


@page_viewer.route('/about')
def about_us():
    return render_template('pages/about_us.html')
