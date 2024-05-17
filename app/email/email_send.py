#!/usr/bin/env python3
from flask import Flask 
from flask_mail import Mail, Message
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Mail
mail = Mail(app)

@app.route('/email', methods=['GET', 'POST'])
def send_email():
    try:
        msg = Message('Hello Obiamaka!',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=['nkolikaveronica7@gmail.com'])
        msg.body = 'I am just trying to test this!'

        mail.send(msg)

        return 'Email has been sent!'
    except Exception as e:
        return f'Email failed to send: {str(e)}'