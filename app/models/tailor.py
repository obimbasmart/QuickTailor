#!/usr/bin/python

"""Tailor Model
"""

from sqlalchemy import String, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base_model import BaseModel
from .base_user import BaseUser

class Tailor(BaseUser, BaseModel):
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
    
    # relationships
    products = relationship("Product", back_populates="tailor")

    # Password reset attributes
    reset_token: Mapped[str] = mapped_column(String(128), nullable=True)
    reset_token_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    @property
    def is_tailor(self):
        return True


