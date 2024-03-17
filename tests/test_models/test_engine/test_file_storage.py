#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_dataModel(unittest.TestCase):
    """Unittests for testing data model of FileStorage class."""

    def test_FileStorage_error_dataType(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_dataMTypes(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    classes = [BaseModel, User, State, City, Amenity, Review]

    @classmethod
    def setUp(self):
        """test set up
            Rename storage file
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """test clean up
            remove test_storage file
            restore storage file
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}


    def test_FileStorage_method_errorDataTypeA(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)
            models.storage.new(BaseModel(), 1)
            models.storage.save(None)

    def test_FileStorage_method_errorDataTypeB(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)
            
    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

   
    def test_reload(self):
        test_obj =[]
        for x in  self.classes:
            obj = x()
            models.storage.new(obj)
            test_obj.append(obj)
            obj.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        for obj in test_obj:
            self.assertIn(f'{obj.__class__.__name__}.' + obj.id, objs)
    
    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_save(self):
        test_obj =[]
        for x in  self.classes:
            obj = x()
            models.storage.new(obj)
            test_obj.append(obj)
        models.storage.save()
        save_objs = ""
        with open("file.json", "r") as f:
            save_objs = f.read()
        for obj in test_obj:
            self.assertIn(f'{obj.__class__.__name__}.' + obj.id,  save_objs)


    def test_new(self):
        for x in  self.classes:
            obj = x()
            models.storage.new(obj)
            self.assertIn(f'{obj.__class__.__name__}.' + obj.id, models.storage.all().keys())
            self.assertIn(obj, models.storage.all().values())


if __name__ == "__main__":
    unittest.main()
