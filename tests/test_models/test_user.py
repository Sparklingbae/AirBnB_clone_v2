#!/usr/bin/python3
"""Defines unittests for models/user.py.
Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_dataModel(unittest.TestCase):
    """Unittests for testing data model of FileStorage class."""

    def test_User_error_dataType(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_User_dataMTypes(self):
        self.assertEqual(User, type(User()))
        self.assertIn(User(), models.storage.all().values())
        self.assertEqual(str, type(User().id))
        self.assertEqual(datetime, type(User().created_at))
        self.assertEqual(datetime, type(User().updated_at))
        self.assertEqual(str, type(User.email))
        self.assertEqual(str, type(User.first_name))
        self.assertEqual(str, type(User.last_name))
        self.assertEqual(str, type(User.password))

    def test_created_at(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)
    
    def test_updated_at(self):
        obj1 = User()
        upd1 = obj1.updated_at
        sleep(0.05)
        setattr(obj1, 'name', 'test')
        obj1.save()
        upd2 = obj1.updated_at
        self.assertLess(upd1, upd2)
    
    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        obj =User()
        obj.id = "a9957-165a-49ea-966f-a0de45"
        obj.created_at = obj.updated_at = dt
        objstr = obj.__str__()
        self.assertIn("[User] (a9957-165a-49ea-966f-a0de45)", objstr)
        self.assertIn("'id': 'a9957-165a-49ea-966f-a0de45'", objstr)
        self.assertIn("'created_at': " + dt_repr, objstr)
        self.assertIn("'updated_at': " + dt_repr, objstr)

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        idd = "a9957-165a-49ea-966f-a0de45"
        obj = User(id=idd, created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(obj.id, idd)
        self.assertEqual(obj.created_at, dt)
        self.assertEqual(obj.updated_at, dt)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save method of the User class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save(self):
        obj = User()
        sleep(0.05)
        first_updated_at = obj.updated_at
        obj.save()
        second_updated_at = obj.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        obj.save()
        self.assertLess(second_updated_at, obj.updated_at)

    def test_save_with_error_arg(self):
        obj = User()
        with self.assertRaises(TypeError):
            obj.save(None)

    def test_save_storage_file(self):
        obj = User()
        obj.save()
        bmid = "User." + obj.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())
    


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        bm = User()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        obj = User()
        self.assertIn("id", obj.to_dict())
        self.assertIn("created_at", obj.to_dict())
        self.assertIn("updated_at", obj.to_dict())
        self.assertIn("__class__", obj.to_dict())

    def test_to_dict_contains_added_attributes(self):
        obj = User()
        obj.name = "alx"
        obj.my_number = 777
        self.assertIn("name", obj.to_dict())
        self.assertIn("my_number", obj.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        obj = User()
        obj_dict = obj.to_dict()
        self.assertEqual(str, type(obj_dict["created_at"]))
        self.assertEqual(str, type(obj_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        obj = User()
        obj.id = "123456"
        obj.created_at = obj.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(obj.to_dict(), tdict)

    

    def test_to_dict_with_error_arg(self):
        obj = User()
        with self.assertRaises(TypeError):
            obj.to_dict(None)


if __name__ == "__main__":
    unittest.main()
