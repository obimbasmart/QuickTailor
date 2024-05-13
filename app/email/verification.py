from app.email import email_views


@email_views.route("/send_mail")
def send_emaial():
    return "<h1>Email has been sent</h1>"