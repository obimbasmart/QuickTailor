from sqlalchemy import  String, Enum, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.base_model import BaseModel


orderStatus = Enum(
    'PENDING', 'COMFIRMED',
    'COMPLETED', 'IN_PRGRESS',
    'DELIVERED',
    name = 'orderStatus'
)

orderProgress = Enum(
    'AWAITING_COMFIRMATION', 'MATERIAL_SOURCING',
    'CUTTING','SEWING', 'IRONING', 'PACKAGING',
    name='orderProgress'
)

class Order(BaseModel):
    __tablename__ = 'orders'
    product_id: Mapped[str] = mapped_column(String(128), ForeignKey('products.id'))
    user_id: Mapped[str] = mapped_column(String(128), ForeignKey('users.id'))
    order_status: Mapped[Enum] = mapped_column(orderStatus, default='PENDING')
    order_progress: Mapped[Enum] = mapped_column(orderProgress, default='AWAITING_COMFIRMATION')
    measurements = mapped_column(JSON, nullable=False)