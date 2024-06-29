"""Product Review class"""

from sqlalchemy import  String, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'
    order_id: Mapped[str] = mapped_column(String(128), ForeignKey('orders.id'))
    product_id: Mapped[str] = mapped_column(String(128), ForeignKey('products.id'))
    review: Mapped[str] = mapped_column(String(1028), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    #relationship
    order = relationship('Order', uselist=False)
    product = relationship('Product', back_populates='reviews')
