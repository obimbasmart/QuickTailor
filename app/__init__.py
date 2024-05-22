#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from app.config import DevConfig, Config, ProdConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv
from flask_login import LoginManager


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

    return app

config = DevConfig
if getenv("APP_ENV") == "production":
    config = ProdConfig

app = create_app(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'app.auth_views.login'

# Import for models are done here to prevent circular import error
from .models.user import User
from .models.tailor import Tailor
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    tailor = Tailor.query.get(user_id)
    return tailor.to_dict() if tailor is not None else user.to_dict()
