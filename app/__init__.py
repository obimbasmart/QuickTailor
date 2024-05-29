#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from app.config import DevConfig, Config, ProdConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_login import current_user
from app.constants import USER_SIDEBAR_LINKS, ADMIN_SIDEBAR_LINKS
from flask_wtf.csrf import CSRFProtect
from cloud_storage.s3_cloud_storage import S3StorageService
from babel.numbers import format_currency


load_dotenv()

def create_app(config=None) -> Flask:
    """create a flask app"""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config)

    @app.errorhandler(404)
    def resource_not_found(self):
        """handle 404 error"""
        return make_response(jsonify({"error": "Not found"}), 404)
    
    @app.context_processor
    def inject_sidebar_links():
        if not current_user.is_anonymous and current_user.is_tailor:
            if current_user.is_tailor:
                return dict(user_sidebar_links=ADMIN_SIDEBAR_LINKS)
        return dict(user_sidebar_links=USER_SIDEBAR_LINKS)
    
    @app.template_filter('currency')
    def currency_filter(value):
        value = int(float(value))
        return format_currency(number=value, currency='NGN',  format=u'¤#,##0',  currency_digits=False)
    return app

config = DevConfig
if getenv("APP_ENV") == "production":
    config = ProdConfig

app = create_app(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth_views.login'
s3_client = S3StorageService('quicktailor-products-bucket')

from app.models.user import User
from app.models.tailor import Tailor

@login_manager.user_loader
def load_user(id: str):
    user = db.session.get(User, id)
    if user is not None:
        return user
    return db.session.get(Tailor, id)
csrf = CSRFProtect(app) #!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from app.config import DevConfig, Config, ProdConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_login import current_user
from app.constants import USER_SIDEBAR_LINKS, ADMIN_SIDEBAR_LINKS
from flask_wtf.csrf import CSRFProtect
from cloud_storage.s3_cloud_storage import S3StorageService
from babel.numbers import format_currency


load_dotenv()

def create_app(config=None) -> Flask:
    """create a flask app"""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config)

    @app.errorhandler(404)
    def resource_not_found(self):
        """handle 404 error"""
        return make_response(jsonify({"error": "Not found"}), 404)
    
    @app.context_processor
    def inject_sidebar_links():
        if not current_user.is_anonymous and current_user.is_tailor:
            if current_user.is_tailor:
                return dict(user_sidebar_links=ADMIN_SIDEBAR_LINKS)
        return dict(user_sidebar_links=USER_SIDEBAR_LINKS)
    
    @app.template_filter('currency')
    def currency_filter(value):
        value = int(float(value))
        return format_currency(number=value, currency='NGN',  format=u'¤#,##0',  currency_digits=False)
    return app

config = DevConfig
if getenv("APP_ENV") == "production":
    config = ProdConfig

app = create_app(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth_views.login'
s3_client = S3StorageService('quicktailor-products-bucket')

from app.models.user import User
from app.models.tailor import Tailor

@login_manager.user_loader
def load_user(id: str):
    user = db.session.get(User, id)
    if user is not None:
        return user
    return db.session.get(Tailor, id)
csrf = CSRFProtect(app) 
