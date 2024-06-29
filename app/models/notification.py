from sqlalchemy import  String, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base_model import BaseModel

class Notification(BaseModel):
    __tablename__ = 'notifications'

    user_id: Mapped[str] = mapped_column(String(128), ForeignKey('users.id'), nullable=True)
    tailor_id:  Mapped[str] = mapped_column(String(128), ForeignKey('tailors.id'), nullable=True)
    sender_user_id: Mapped[str] = mapped_column(String(128), ForeignKey('users.id'), nullable=True)
    sender_tailor_id: Mapped[str] = mapped_column(String(128), ForeignKey('tailors.id'), nullable=True)
    product_id: Mapped[str] = mapped_column(String(128), ForeignKey('products.id'), nullable=True)
    content: Mapped[str] = mapped_column(String(128), nullable=False)
    message_id: Mapped[str] = mapped_column(String(128), ForeignKey('messages.id'), nullable=True)
    is_clicked = mapped_column(Boolean, default=False)
    is_user = mapped_column(Boolean, default=False)
    url:  Mapped[str] = mapped_column(String(128),  nullable=False)

    # relationships
    product_notification = relationship('Product', back_populates='notification')
    message_notification = relationship('Message', back_populates='notification')
    sender_user = relationship('User', foreign_keys=[sender_user_id], back_populates='notification_sent')
    sender_tailor = relationship('Tailor', foreign_keys=[sender_tailor_id], back_populates='notification_sent')
    user_notification= relationship('User', foreign_keys=[user_id], back_populates='notification')
    tailor_notification = relationship('Tailor',foreign_keys=[tailor_id],  back_populates='notification')
