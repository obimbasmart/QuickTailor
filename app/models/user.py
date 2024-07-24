#!/usr/bin/python

"""User Model
"""

from ..models.base_user import BaseUser
from sqlalchemy.orm import Mapped, mapped_column
from ..models.base_model import BaseModel
from sqlalchemy import JSON, String, DateTime, TEXT, Integer
from sqlalchemy.orm import mapped_column, relationship
from app.constants import default_measurement
from sqlalchemy_json import NestedMutableJson

class User(BaseModel, BaseUser):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
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

  # Relationship with Message & MessageList
    message_sent = relationship('Message',foreign_keys= "Message.sender_user_id", back_populates='sender_user')
    message_recieved = relationship('Message', foreign_keys= "Message.reciever_user_id",  back_populates='reciever_user')
    message_list = relationship('MessageList',   back_populates='user')

    # Relationship with Notification
    notification = relationship('Notification',foreign_keys="Notification.user_id",  back_populates='user_notification')
    notification_sent = relationship('Notification',foreign_keys= "Notification.sender_user_id", back_populates='sender_user')

