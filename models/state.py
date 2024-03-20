#!/usr/bin/python3
"""Defines the State class."""
from models.base_model import BaseModel, Base
from models import storage
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """Represent a state.
    Attributes:
        name (str): The name of the state.
    """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """get a list of all related city instances
            with state_id = to the current state id
            """
            cities_list = []

            for city in [*storage.all(City).values()]:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
