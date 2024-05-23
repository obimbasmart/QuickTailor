
"""
Index
"""


from flask_login import current_user
from flask import render_template
from app.views import app_views


@app_views.route("/")
def home():
    print(current_user)
    return render_template('pages/home.html',page='home', current_user=current_user)

@app_views.route("/how-it-works")
def how_it_works():
    return render_template('pages/howItWorks.html',page='how it works')


@app_views.route("/register")
def register():
    return render_template('pages/register.html',page='home')

@app_views.route('/about')
def about_us():
    return render_template('pages/about_us.html')



