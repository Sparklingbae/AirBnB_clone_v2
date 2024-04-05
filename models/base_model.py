#!/usr/bin/python3
"""Defines the BaseModel class."""

from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs) -> None:
        """Initialize a new BaseModel.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self) -> str:
        """Return the print/str representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self) -> None:
        """Update updated_at with the current datetime."""

        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self) -> dict:
        """Return the dictionary of the BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        ret = {'__class__': self.__class__.__name__, **self.__dict__}
        ret["created_at"] = self.created_at.isoformat()
        ret["updated_at"] = self.updated_at.isoformat()
        ret.pop("_sa_instance_state", None)
        return ret

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
