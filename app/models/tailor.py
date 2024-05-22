#!/usr/bin/python

"""Tailor Model
"""

from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..models.base_model import BaseModel
from .base_user import BaseUser
from flask_login import UserMixin

class Tailor(BaseUser, BaseModel, UserMixin):
    __tablename__ = 'tailors'

    #basic attrs
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    phone_no: Mapped[str] = mapped_column(String
                                          (128), nullable=False)

    # tailor attrs
    business_name: Mapped[str] = mapped_column(String(128), nullable=True)
    state: Mapped[str] = mapped_column(String(128), nullable=True)
    city: Mapped[str] = mapped_column(String(128), nullable=True)
    street: Mapped[str] = mapped_column(String(128), nullable=True)
    is_available = mapped_column(Boolean, default=True)
    no_of_completed_jobs: Mapped[int] = mapped_column(Integer, default=0)
    reputation: Mapped[int] = mapped_column(Integer, nullable=True)


