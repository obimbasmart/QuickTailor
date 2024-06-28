#!/usr/bin/env python3
"""routes specific for tailors alone"""

from flask import Blueprint

tailor_views = Blueprint("tailor_views", __name__)

from . import verification
from . import index
from . import CRUD
from . import orders
from . import profile