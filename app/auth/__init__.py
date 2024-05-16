#!/usr/bin/env python3
"""initialize authentication module"""

from flask import Blueprint

auth_views = Blueprint("auth_views", __name__)

from . import login

from . import register
