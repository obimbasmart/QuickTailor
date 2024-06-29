from app.views import app_views
from flask import render_template, request
from app.constants import USER_SIDEBAR_LINKS
from cloud_storage.s3_cloud_storage import S3StorageService
from app.views.index import notification
from app.forms.cart_forms import CustomizationForm
from flask_socketio import SocketIO, send
from app import socketio

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

@app_views.route('/messages', methods=['GET', 'POST'])
def messages():
    return render_template('pages/chat.html')
