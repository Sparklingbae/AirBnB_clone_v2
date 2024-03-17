#!/usr/bin/python3
"""Defines the self class."""

from json import dump, load
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity


class FileStorage:
    """Represent an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self) -> dict:
        """Return the dictionary __objects."""
        return self.__objects

    def new(self, obj: object) -> None:
        """Set in __objects obj with key <obj_class_name>.id"""
        key = f'{obj.__class__.__name__}.{obj.id}'
        self.__objects.update({key: obj})

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        with open(self.__file_path, 'w') as file:
            ret = {}

            for key, value in self.__objects.items():
                ret.update({key: value.to_dict()})

            dump(ret, file, indent=4)

    def reload(self) -> None:
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, 'r') as file:
                objs = load(file)
            for key, value in objs.items():
                cls = eval(value['__class__'])
                self.new(cls(**value))

        except FileNotFoundError:
            pass
