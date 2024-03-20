#!/usr/bin/python3
"""__init__ magic method for models directory
    loading objects storage
"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
