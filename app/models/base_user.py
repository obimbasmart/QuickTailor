#!/usr/bin/python

"""Abstract User
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta
from app import db
from app import app
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


class BaseUser(UserMixin):

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self):
        token = serializer.dumps(self.id, salt='password-reset-salt')
        self.reset_token = token
        self.reset_token_expires = datetime.utcnow(
        ) + timedelta(hours=1)  # Token valid for 1 hour
        db.session.commit()
        return token

    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expires = None
        db.session.commit()

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = serializer.loads(token, salt="password-reset-salt", max_age=3600)
        except:
            return None

        from app.models.tailor import Tailor
        from app.models.user import User

        normal_user = db.session.get(User, id)
        tailor = db.session.get(Tailor, id)

        return normal_user or tailor
    
    @property
    def is_tailor(self):
        return False
