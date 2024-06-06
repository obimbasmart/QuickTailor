#!/usr/bin/env python3

"""App Configurations
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
    ADMINS = os.getenv('ADMINS')

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
