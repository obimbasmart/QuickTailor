#!/usr/bin/python

"""Abstract User
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta
from app import db




class BaseUser(UserMixin):

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_token(self, token):
        self.reset_token = token
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
        db.session.commit()

    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expires = None
        db.session.commit()
~
~
    @property
    def is_tailor(self):
        return False
