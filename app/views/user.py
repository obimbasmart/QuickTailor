

from flask import render_template
from app.views import app_views
from app.constants import USER_SIDEBAR_LINKS

@app_views.route('/yomi-casual')
def tailor_profile():
    return render_template('pages/tailor_profile.html', 
                           user_sidebar_links=USER_SIDEBAR_LINKS)