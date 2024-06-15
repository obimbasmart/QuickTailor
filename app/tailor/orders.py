"""
Order views
"""


from app.tailor import tailor_views
from app.auth.decorators import tailor_required
from flask import request, redirect, abort
from app.models.order import Order
from datetime import datetime
from app.models import db
from flask_login import current_user
from email_service.sendgrid import send_order_comfirmation_email, send_order_completion_email
import os


@tailor_views.route("/order/<order_id>", methods=["POST"])
@tailor_required
def update_order(order_id=None):
    stage = int(request.form.get('stage').split('_')[1])
    order = Order.query.filter_by(id=order_id).one_or_404()

    # ensure previous step have been updated
    if stage != 0 and order.stages[stage - 1]['status'] == 'pending':
        abort(400)

    order.stages[stage]['updated_at'] = str(datetime.utcnow())
    order.stages[stage]['status'] = 'completed'

    if stage == 0:
        order.status = 'IN PROGRESS'
        db.session.commit()

        # TODO: send email to user when order is comfirmed
        if os.environ.get('APP_ENV') not in "testing":
            send_order_comfirmation_email(order.user, order)
        return redirect(request.referrer)

    if stage == 4:
        order.status = 'COMPLETED'
        # TODO: send email to user when order is completed
        if os.environ.get('APP_ENV') not in "testing":
            send_order_completion_email(order.user, order)

    db.session.commit()
    return f'<button disable type="button" class="border-[1px] border-pc-teal-normal text-pc-teal-normal bg-white text-xs tracking-wide   focus:outline-none  dark:focus:ring-teal-800 font-medium rounded-lg px-4 py-2 text-center">Updated</button>'
