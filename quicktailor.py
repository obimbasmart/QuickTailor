from app import app
from app.views import app_views
from app.auth import auth_views
from app.sendgrid import email_service
from app.About_us import page_viewer


app.register_blueprint(app_views)
app.register_blueprint(auth_views)
app.register_blueprint(email_service)
app.register_blueprint(page_viewer)