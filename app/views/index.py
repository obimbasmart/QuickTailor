
"""
Index
"""

from app.constants import USER_SIDEBAR_LINKS


from flask import render_template
from app.views import app_views


@app_views.route("/")
def home():
    return render_template('pages/home.html',
                           user_sidebar_links = USER_SIDEBAR_LINKS)