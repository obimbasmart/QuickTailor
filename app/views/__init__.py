#!/usr/bin/env python3
"""initialize app views"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__)


from . import index
from . import product
from . import user
from . import cart_save
from . import payment
from . import measurement
from . import order