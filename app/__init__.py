#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from app.config import DevConfig, Config, ProdConfig
from  flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv


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
mail = Mail(app)
