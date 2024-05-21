
"""
Index
"""

from app.constants import USER_SIDEBAR_LINKS


from flask import render_template
from app.views import app_views


@app_views.route("/")
def home():
    return render_template('pages/home.html',
                           user_sidebar_links = USER_SIDEBAR_LINKS, page='home')

@app_views.route("/how-it-works")
def how_it_works():
    return render_template('pages/howItWorks.html',
                           user_sidebar_links = USER_SIDEBAR_LINKS, page='how it works')


@app_views.route("/register")
def register():
    return render_template('pages/register.html',
                           user_sidebar_links = USER_SIDEBAR_LINKS, page='home')


