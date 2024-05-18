

from app import mail
from app.email import email_views
from flask_mail import Message
from os import getenv

@email_views.route("/send_mail")
def send_email():
    msg = Message(subject="SEnt from SEndrig QT",
                  recipients=["obimbasmartchukwunenye@gmail.com"],
                  body="We are just testing stuffs",
                  html="<h1>This iis hte html </h1>",
                  sender=getenv("MAIL_DEFAULT_SENDER"))
    
    mail.send(msg)
