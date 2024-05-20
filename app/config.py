#!/usr/bin/env python3

"""App Configurations
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0

# Flask-Mail Configurations
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 25
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}/{}'.format(os.environ.get("MYSQL_USER"),
                                                                   os.environ.get(
                                                                       "MYSQL_PWD"),
                                                                   os.environ.get(
                                                                       "MYSQL_HOST"),
                                                                   os.environ.get(
                                                                       "MYSQL_DB"))
