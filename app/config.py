#!/usr/bin/env python3

"""App Configurations
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)
    
def create_db_url(user, pwd, host, db):
    return f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'

def get_env_db_url(env_setting):
    MYSQL_USER = get_env_variable("MYSQL_USER")
    MYSQL_PWD = get_env_variable("MYSQL_PWD")
    MYSQL_HOST = get_env_variable("MYSQL_HOST")

    if env_setting == "development":
       MYSQL_DB = get_env_variable('MYSQL_DEV_DB')
    elif env_setting == "testing":
        MYSQL_DB = get_env_variable('MYSQL_TEST_DB')
    elif env_setting == "production":
        MYSQL_DB = get_env_variable('MYSQL_DB')

    return create_db_url(MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB)


# DB URLS for each Environment
DEV_DB_URL = get_env_db_url("development")
TESTING_DB_URL = get_env_db_url("testing")
PROD_DB_URL = get_env_db_url("production")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
    ADMINS = os.getenv('ADMINS')

    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    WTF_CSRF_ENABLED=False
    TESTING = True