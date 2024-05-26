#!/usr/bin/env python3

import os
from flask import render_template
from app.order_manager import order_views


@order_views.route('/track-order')
def order_tracker():
    return render_template('pages/track_order.html')