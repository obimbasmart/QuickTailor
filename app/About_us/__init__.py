#!/usr/bin/env/ python3
"""initialize the pages module to help in handling pages urls"""

from flask import Blueprint

page_viewer = Blueprint("page_viewer", __name__)

from . import about_us
from . import notification