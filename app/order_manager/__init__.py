#!/usr/bin/env/ python3
"""Help to handle routes relating to orders and tracking """

from flask import Blueprint

order_views = Blueprint("order_views", __name__)

from . import order_tracker