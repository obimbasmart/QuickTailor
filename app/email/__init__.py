#!/usr/bin/python3
"""initialize view module"""

from flask import Blueprint

email_views = Blueprint("email_views", __name__)

from . import send_email
from . import send_passowrd_mail