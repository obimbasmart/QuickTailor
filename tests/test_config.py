"""
    Tet app client configurations
"""

from app.config import get_env_db_url

def test_testing_config(app):
    DB_URL = get_env_db_url('testing')
    assert app.config['SQLALCHEMY_DATABASE_URI'] == DB_URL
    assert app.config["DEBUG"]
    assert app.config["TESTING"]
