from sqlalchemy import  String, Enum, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import BaseModel


class CartItem(BaseModel):
    __tablename__ = 'carts'
    product_id: Mapped[str] = mapped_column(String(128), ForeignKey('products.id'))
    user_id: Mapped[str] = mapped_column(String(128), ForeignKey('users.id'))
    measurements = mapped_column(JSON, nullable=False)
    cusomization_value: Mapped[str] = mapped_column(String(128), nullable=True)

    # relationship
    product = relationship("Product", uselist=False)