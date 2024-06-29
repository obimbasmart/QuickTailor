#!/usr/bin/python

"""User Model
"""

from ..models.base_user import BaseUser
from sqlalchemy.orm import Mapped, mapped_column
from ..models.base_model import BaseModel
from sqlalchemy import JSON, String, DateTime, TEXT, Integer
from sqlalchemy.orm import mapped_column
from app.constants import default_measurement
from sqlalchemy_json import NestedMutableJson

class User(BaseModel, BaseUser):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password_hash: Mapped[str] = mapped_column(TEXT(), nullable=False)
    phone_no: Mapped[str] = mapped_column(String(128), nullable=False)

    measurements = mapped_column(JSON, nullable=True,
            default=default_measurement)
    
    # Password reset attributes
    reset_token: Mapped[str] = mapped_column(String(128), nullable=True)
    reset_token_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    otp: Mapped[int] = mapped_column(Integer, nullable=True)

    saved_items = mapped_column(NestedMutableJson, default=[])

