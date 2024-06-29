from sqlalchemy import String, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base_model import BaseModel
import json


class Product(BaseModel):
    __tablename__ = 'products'
    tailor_id: Mapped[str] = mapped_column(
        String(128), ForeignKey('tailors.id'))
    name: Mapped[str] = mapped_column(String(128), nullable=True)
    description: Mapped[str] = mapped_column(String(350), nullable=True)
    price: Mapped[str] = mapped_column(String(128), nullable=False)
    images = mapped_column(JSON, default={})
    estimated_tc: Mapped[int] = mapped_column(Integer, nullable=False)
    material: Mapped[str] = mapped_column(String(128), nullable=True)
    on_draft: Mapped[bool] = mapped_column(Boolean)

    # relationships
    tailor = relationship("Tailor", back_populates="products")
    reviews = relationship('Review', back_populates='product', lazy='joined')
    product_msg = relationship('Message',  back_populates="product")
    notification= relationship("Notification", back_populates="product_notification")


    # codes
    customization_tokens = mapped_column(JSON, default={})

    @property
    def img(self):
        from app import s3_client
        return s3_client.generate_presigned_url('get_object', list(self.images.values())[0])

    """
        Note: Thi property was only implemented to help build the feature of Saved Items
    """
    @property
    def to_json(self):
        valid_keys = ['id']
        attrs = {
            key: val for key, val in self.to_dict().items()
            if key in valid_keys
        }

        return json.dumps(attrs)
