from app.tailor import tailor_views
from app.auth.decorators import tailor_required
from app.models import db
from flask_login import current_user


@tailor_views.route("/tailor/availability", methods=["GET"])
@tailor_required
def update_availability():
    current_user.is_available = not current_user.is_available
    db.session.commit()
    return ""
    