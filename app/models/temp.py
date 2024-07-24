
""" Manages temporary data for unregistered users, including
    registration tokens and saved items, providing a unified 
    interface for anonymous user interactions.
"""

from  app.models.base_model import BaseModel
from sqlalchemy import String
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import Mapped, mapped_column
from ..models.base_model import BaseModel

class AnonymousUserRecord(BaseModel):
    __tablename__ = 'anonymous_users'
    ip: Mapped[str] = mapped_column(String(128), nullable=True)
    data = mapped_column(NestedMutableJson, default={})