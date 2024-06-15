from sqlalchemy import  String, Enum, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import NestedMutableJson
from ..models.base_model import BaseModel


orderStatus = Enum(
    'PENDING', 'COMFIRMED',
    'COMPLETED', 'IN PROGRESS',
    'DELIVERED',
    name = 'orderStatus'
)

stages_names = ['Order comfirmed', 'Material sourcing',
          'Sewing', 'Packaging', 'Ready for pickup'
         ]

stages = [
        {
            'name' : stage_name,
            'status': 'pending',
            'updated_at': 'N/A'
        }

        for stage_name in stages_names
]

class Order(BaseModel):
    __tablename__ = 'orders'
    product_id: Mapped[str] = mapped_column(String(128), ForeignKey('products.id'))
    user_id: Mapped[str] = mapped_column(String(128), ForeignKey('users.id'))
    status: Mapped[Enum] = mapped_column(orderStatus, default='PENDING')
    stages = mapped_column(NestedMutableJson, nullable=False, default=stages)
    measurements = mapped_column(JSON, nullable=False)

    # relationship
    product = relationship('Product', uselist=False)
    user = relationship('User', uselist=False)