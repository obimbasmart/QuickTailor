from app import app
from app.views import app_views
from app.auth import auth_views
from app.email import email_service
from app.About_us import page_viewer
<<<<<<< HEAD
from app.order_manager import order_views

=======
from app.tailor import tailor_views
>>>>>>> b7302414251aa02f75a6b61e539244f79f61595e

app.register_blueprint(app_views)
app.register_blueprint(auth_views)
app.register_blueprint(email_service)
app.register_blueprint(page_viewer)
<<<<<<< HEAD
app.register_blueprint(order_views)
=======
app.register_blueprint(tailor_views)
>>>>>>> b7302414251aa02f75a6b61e539244f79f61595e
