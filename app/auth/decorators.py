

from functools import wraps
from flask_login import current_user, login_required
from flask import abort

def tailor_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_tailor:
            return abort(404)  # Forbidden or not Found
        return f(*args, **kwargs)
    return decorated_function