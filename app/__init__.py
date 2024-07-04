#!/usr/bin/env python3

from app.models.tailor import Tailor
from app.models.user import User
from flask import Flask, jsonify, make_response
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig
from flask_migrate import Migrate
from os import environ
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_login import current_user
from app.constants import USER_SIDEBAR_LINKS, ADMIN_SIDEBAR_LINKS
from flask_wtf.csrf import CSRFProtect
from app.cloud_storage.s3_cloud_storage import S3StorageService
from app.cache import Cache
from app.forms.tailor_forms import CRSForm
from flask_socketio import SocketIO


load_dotenv()

migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
redis_cache = Cache()
s3_client = S3StorageService('quicktailor-products-bucket', cache=redis_cache)
socketio = SocketIO()
if __name__ == '__main__':
        socketio.run(app, debug=True)


def create_app(config=DevelopmentConfig) -> Flask:
    """create a flask app"""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    if environ['APP_ENV'] == 'production':
        config = ProductionConfig
    app.config.from_object(config)

    from app.models import db
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

        login_manager.init_app(app)
        login_manager.login_view = 'auth_views.login'

        csrf.init_app(app)
        socketio.init_app(app)
        register_blueprints(app)
        register_filters(app)
        app.config['db'] = db

                                          
    @app.context_processor
    def inject_sidebar_links():
        if not current_user.is_anonymous and current_user.is_tailor:
            if current_user.is_tailor:
                return dict(user_sidebar_links=ADMIN_SIDEBAR_LINKS)
        return dict(user_sidebar_links=USER_SIDEBAR_LINKS, crsf=CRSForm())

    @app.errorhandler(404)
    def resource_not_found(self):
        """handle 404 error"""
        return make_response(jsonify({"error": "Not found"}), 404)

    return app


@login_manager.user_loader
def load_user(id: str):
    from app.models import db
    user = db.session.get(User, id)
    if user is not None:
        return user
    return db.session.get(Tailor, id)


def register_filters(app):
    import app.filters as filters
    app.jinja_env.filters['currency'] = filters.currency_filter
<<<<<<< HEAD
    app.jinja_env.filters['now'] = filters.now_utc
=======
>>>>>>> a03186c2a9fa59fe5729ea032872dd4f8985783d
    app.jinja_env.filters['timeago'] = filters._timeago
    app.jinja_env.filters['custom_timeago'] = filters.custom_timeago
    app.jinja_env.filters['custom_time'] = filters.custom_time_format
    app.jinja_env.filters['tolist'] = filters.tolist
    app.jinja_env.filters['sum_price'] = filters.sum_price
    app.jinja_env.filters['sum_custom_value'] = filters.sum_custom_value
    app.jinja_env.filters['to_datetime'] = filters.format_datetime
    app.jinja_env.filters['completion_date'] = filters.completion_date
    app.jinja_env.filters['is_date_more_than_days_ago'] = filters.is_date_more_than_days_ago
    app.jinja_env.filters['to_date_dmy'] = filters.to_date_dmy
    app.jinja_env.filters['time_now'] = filters.time_now
    app.jinja_env.filters['today_date'] = filters.today_date
    app.jinja_env.filters['average_reviews'] = filters.average_reviews


def register_blueprints(app):
    from app.views import app_views
    from app.auth import auth_views
    from app.email import email_service
    from app.notification import page_viewer
    from app.order_manager import order_views
    from app.tailor import tailor_views

    app.register_blueprint(app_views)
    app.register_blueprint(auth_views)
    app.register_blueprint(email_service)
    app.register_blueprint(page_viewer)
    app.register_blueprint(order_views)
    app.register_blueprint(tailor_views)
    
