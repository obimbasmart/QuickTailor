

from app.auth import auth_views


@auth_views.route("/login")
def login():
    return '<h1>User has logged in</h1>'