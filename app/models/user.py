#!/usr/bin/python

"""User Model
"""

from ..models.base_user import BaseUser
from sqlalchemy.orm import Mapped, mapped_column
from ..models.base_model import BaseModel
from sqlalchemy import JSON, String
from sqlalchemy.orm import mapped_column
from app.constants import default_measurement

class User(BaseModel, BaseUser):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    phone_no: Mapped[str] = mapped_column(String(128), nullable=False)

    measurements = mapped_column(JSON, nullable=True,
                                 default=default_measurement)
