#!/usr/bin/env python3

""" login route """
from app.auth import auth_views

from flask import request, render_template
from app.constants import USER_SIDEBAR_VISITORS

@auth_views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('pages/login.html',
                           user_sidebar_links = USER_SIDEBAR_VISITORS)

