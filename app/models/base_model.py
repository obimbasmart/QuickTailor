#!/usr/bin/env python3

"""BaseModel Module
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from datetime import datetime, timezone
from app import db


class BaseModel(db.Model):
    __abstract__ = True
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),
                                                 onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
    
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if "password_hash" in new_dict:
            del new_dict["password_hash"]
        return new_dict
