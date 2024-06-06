
""" SendGrid email for service for managing email requests
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import List
from flask import render_template
from app import app


def send_email(subject: str, body: str, recievers: List[str], html_content=None) -> int:
    message = Mail(
        from_email=os.getenv('MAIL_DEFAULT_SENDER'),
        to_emails=recievers,
        subject=subject,
        plain_text_content=body,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(e)
        return 500


def send_password_reset_email(user):
    token = user.generate_reset_token()
    send_email(
        subject='[QuickTailor] Reset Password',
        recievers=[user.email],
        body=render_template('emails/reset_password.txt',
                                           user=user, token=token))
