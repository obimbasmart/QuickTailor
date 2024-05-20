#!/usr/bin/env python3

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Content, Mail
from app.sendgrid import email_service



@email_service.route('/email')
def send_email():
   
    
    mail = Mail(
    from_email=os.environ.get('MAIL_DEFAULT_SENDER'),
    to_emails='obiamaka0101@gmail.com',
    subject='Testing out Twilio SendGrid',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "Sucess"

       
    except Exception as e:
        print(e)
        return "Error"