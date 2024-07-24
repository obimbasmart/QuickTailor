from flask import render_template, redirect, request, jsonify
from flask_login import current_user, login_required
from app.views import app_views
from app.models.notification import Notification
from app.models import db

@app_views.route('/notifications/<id_notify>')
@login_required
def user_notifications(id_notify=None):

    if id_notify is None:
        return render_template('pages/notification.html', current_user = current_user.to_dict())
    else:

        # Find the notification by ID
        notification = Notification.query.get(id_notify)
        if notification:
        # Update the is_click status
            notification.is_clicked = True
            db.session.commit()
            return redirect(notification.url)
        else:
        # Handle the case where the notification is not found
            return render_template('pages/notification.html', current_user = current_user.to_dict())
@app_views.route('/notifications')
@login_required
def notifications():
        a = current_user.notification
        
        for e in a :
            print(e.to_dict())
            #db.session.delete(e)
        #db.session.commit()
        return render_template('pages/notification.html')

@app_views.route('/get_notifications')
@login_required
def get_notifications():
    notify = current_user.notification
    notification = sorted(notify, key=lambda notif: notif.created_at)
    formatted_notifications = [content.to_dict() for content in notification]

    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_notifications = formatted_notifications[start:end]
    return jsonify(paginated_notifications)
