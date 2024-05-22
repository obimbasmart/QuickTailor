#!/usr/bin/env/ python3
"""initialize email_service module"""

from flask import Blueprint

email_service = Blueprint("email_service", __name__)

from . import email