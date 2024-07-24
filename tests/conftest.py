
"""
Test Fixtures
"""

from app import create_app
from app.models import db
import pytest
from app.models.user import User
from app.config import TestingConfig
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope='module')
def new_user():
    user = User(email='obimbasmartchukwunenye@gmail.com', phone_no='08130119931',
                first_name='oleg', last_name='byonic', password='1234')
    return user


@pytest.fixture(scope='module')
def app():
    app = create_app(TestingConfig)
    with app.app_context():
       #always starting with an empty DB
        db.create_all()
        yield app
        # clean up db
        db.session.remove()
        db.drop_all()
        # if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        #     db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def _db(app):
    return app.config['db']