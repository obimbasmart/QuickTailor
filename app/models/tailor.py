#!/usr/bin/python

"""Tailor Model
"""

from sqlalchemy import String, Boolean, Integer, DateTime, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base_model import BaseModel
from .base_user import BaseUser
from app.models.product import Product
from app.models.order import Order
from app.models.review import Review
import json
import base64

class Tailor(BaseUser, BaseModel):
    __tablename__ = 'tailors'

    #basic attrs
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password_hash: Mapped[str] = mapped_column(TEXT(), nullable=False)
    phone_no: Mapped[str] = mapped_column(String
                                          (128), nullable=False)

    # tailor attrs
    business_name: Mapped[str] = mapped_column(String(128), nullable=True)
    cac_number: Mapped[str] = mapped_column(String(128), nullable=True)
    about: Mapped[str] = mapped_column(String(1024), nullable=True)
    state: Mapped[str] = mapped_column(String(128), nullable=True)
    city: Mapped[str] = mapped_column(String(128), nullable=True)
    street: Mapped[str] = mapped_column(String(128), nullable=True)
    is_available = mapped_column(Boolean, default=True)
    no_of_completed_jobs: Mapped[int] = mapped_column(Integer, default=0)
    reputation: Mapped[int] = mapped_column(Integer, nullable=True)

    photo_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    
    #bank details
    bank_name: Mapped[str] = mapped_column(String(128), nullable=True)
    account_number: Mapped[int] = mapped_column(Integer, nullable=True)
    account_name: Mapped[str] = mapped_column(String(128), nullable=True)

    # relationships
    products = relationship(Product, back_populates="tailor")

    # Password reset attributes
    reset_token: Mapped[str] = mapped_column(String(128), nullable=True)
    reset_token_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    @property
    def is_tailor(self):
        return True
    
    @property
    def reviews(self):
        return [
            review for review in Review.query.all()
            if review.product.tailor_id == self.id
        ]
    
    @property
    def n_completed_orders(self):
        completed_orders = Order.query.filter_by(status="COMPLETED").all()
        return len([order for order in completed_orders if order.product.tailor_id == self.id])


    @property
    def photo(self):
        from app import s3_client
        try:
            return s3_client.generate_presigned_url('get_object', self.photo_url)
        except Exception as e:
            return "/static/images/default_profile.png"
        
    @classmethod
    def generate_customization_code(cls, product_id: str, value: int):
        attr = json.dumps({"product_id":  product_id, "value": value})
        code = base64.b64encode(attr.encode('utf-8')).decode('utf-8')
        print(code)
        return code

    @classmethod
    def decode_customization_code(cls, code: str):
        decoded_str = base64.b64decode(code).decode('utf-8')
        code = json.loads(decoded_str)
        return code


