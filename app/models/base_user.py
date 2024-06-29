#!/usr/bin/python

"""Abstract User
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from app.models import db
import random

serializer = URLSafeTimedSerializer('xyz')


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
    
    def generate_otp(self):
        otp = random.randint(100000,999999)
        self.otp = otp
        self.reset_token_expires = datetime.utcnow(
        ) + timedelta(hours=1)  # Token valid for 1 hour
        return otp

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
    
    @staticmethod
    def verify_otp(user_id: str, otp: int):
        from app.models.tailor import Tailor
        from app.models.user import User

        normal_user = db.session.get(User, user_id)
        tailor = db.session.get(Tailor, user_id)

        user = normal_user or tailor
        
        return user.otp == otp
    
    @property
    def is_tailor(self):
        return False
