
""" SendGrid email for service for managing email requests
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import List



def send_email(subject: str, body: str, recievers: List[str], html_content=None) -> int:
    message = Mail(
        from_email="emmapromisesmartnbc@gmail.com",
        to_emails=recievers,
        subject=subject,
        plain_text_content=body,
        html_content=html_content)
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(e)