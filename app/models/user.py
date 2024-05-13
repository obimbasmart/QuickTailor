#!/usr/bin/python

"""User Model
"""

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.constants import default_measurement
from ..models.base_model import BaseModel
from time import time

class User(BaseModel):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    phone_no: Mapped[str] = mapped_column(String(128), nullable=True)
    measurements = mapped_column(JSON, nullable=True,
                                 default=default_measurement)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)