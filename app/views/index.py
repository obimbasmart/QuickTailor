
"""
Index
"""


from flask_login import current_user
from flask import render_template, request, jsonify
from app.views import app_views


notification= [
    {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
      {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"},
  {"time": "3hr ago", "content": "The virtues of life if I have the choice of life", "icon": "📥", "time_elapsed": "2 minutes ago"}
]


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

@app_views.route('/get_notifications')
def get_notifications():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_notifications = notification[start:end]
    return jsonify(paginated_notifications)

@app_views.route('/notification')
def notificationn():
    return render_template("pages/notification.html")



