from sqlalchemy import  String, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base_model import BaseModel

class Message(BaseModel):
    __tablename__ = 'messages'

    sender_user_id: Mapped[str] = mapped_column(String(128), ForeignKey('users.id'), nullable=True)
    reciever_user_id: Mapped[str] = mapped_column(String(128), ForeignKey('users.id'), nullable=True)
    sender_tailor_id:  Mapped[str] = mapped_column(String(128), ForeignKey('tailors.id'), nullable=True)
    reciever_tailor_id:  Mapped[str] = mapped_column(String(128), ForeignKey('tailors.id'), nullable=True)
    product_id: Mapped[str] = mapped_column(String(128), ForeignKey('products.id'), nullable=True)
    thread_msg_id: Mapped[str] = mapped_column(String(128),  nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    media_url: Mapped[str]= mapped_column(String(255), nullable=True)
    media_type: Mapped[str]  = mapped_column(String(50), nullable=True)  # 'image' or 'video'
    is_viewed =  mapped_column(Boolean, default=False)

    # relationships
    notification= relationship("Notification", back_populates="message_notification")
    product = relationship('Product', back_populates='product_msg')
    sender_user = relationship('User', foreign_keys=[sender_user_id], back_populates='message_sent')
    reciever_user = relationship('User',  foreign_keys=[reciever_user_id], back_populates='message_recieved')
    sender_tailor = relationship('Tailor', foreign_keys=[sender_tailor_id], back_populates='message_sent')
    reciever_tailor = relationship('Tailor',foreign_keys=[reciever_tailor_id], back_populates='message_recieved')

class MessageList(BaseModel):
    __tablename__ = 'messages_list'

    user_id: Mapped[str] = mapped_column(String(128), ForeignKey('users.id'), nullable=False)
    tailor_id:  Mapped[str] = mapped_column(String(128), ForeignKey('tailors.id'), nullable=False)
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    user_url: Mapped[str]= mapped_column(String(255), nullable=False)
    tailor_url: Mapped[str]= mapped_column(String(255), nullable=False)
    is_viewed =  mapped_column(Boolean, default=False)
    tailor_img_url: Mapped[str]= mapped_column(String(255), nullable=True)
    user_img_url: Mapped[str]= mapped_column(String(255), nullable=True)
    last_sender: Mapped[str] = mapped_column(String(128), nullable=True)




    # relationships
    user = relationship('User', back_populates='message_list')
    tailor = relationship('Tailor',  back_populates='message_list')