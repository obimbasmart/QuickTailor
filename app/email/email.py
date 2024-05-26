#!/usr/bin/env python3

from app.email import email_service
from email_service.sendgrid import send_email
from flask import render_template

@email_service.route('/reset_password')
def _send_email():
    status = send_email(
        subject="[QuickTailor] Password Reset",
        recievers=["Memmalino@gmail.com", 
                   "obiamaka0101@gmail.com",
                   "obimbasmartchukwunenye@gmail.com",
                   "uzochukwu.chikadibia@gmail.com"],
        body=render_template('emails/reset_password.txt'))
    return  f'<h1>Email has beeen send with status: {status}'