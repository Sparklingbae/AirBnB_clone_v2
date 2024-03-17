#!/usr/bin/python3
"""Defines unittests for models/Place.py.
Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_dataModel(unittest.TestCase):
    """Unittests for testing data model of FileStorage class."""

    def test_Place_error_dataType(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    def test_Place_dataMTypes(self):
        self.assertEqual(Place, type(Place()))
        self.assertIn(Place(), models.storage.all().values())
        self.assertEqual(str, type(Place().id))
        self.assertEqual(datetime, type(Place().created_at))
        self.assertEqual(datetime, type(Place().updated_at))
        self.assertEqual(str, type(Place.city_id))
        self.assertEqual(str, type(Place.user_id))
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertEqual(int, type(Place.number_rooms))
        self.assertEqual(float, type(Place.latitude))
        self.assertEqual(float, type(Place.longitude))

    def test_created_at(self):
        obj1 = Place()
        sleep(0.05)
        obj2 = Place()
        self.assertLess(obj1.created_at, obj2.created_at)
    
    def test_updated_at(self):
        obj1 = Place()
        upd1 = obj1.updated_at
        sleep(0.05)
        setattr(obj1, 'name', 'test')
        obj1.save()
        upd2 = obj1.updated_at
        self.assertLess(upd1, upd2)
    
    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        obj =Place()
        obj.id = "a9957-165a-49ea-966f-a0de45"
        obj.created_at = obj.updated_at = dt
        objstr = obj.__str__()
        self.assertIn("[Place] (a9957-165a-49ea-966f-a0de45)", objstr)
        self.assertIn("'id': 'a9957-165a-49ea-966f-a0de45'", objstr)
        self.assertIn("'created_at': " + dt_repr, objstr)
        self.assertIn("'updated_at': " + dt_repr, objstr)

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        idd = "a9957-165a-49ea-966f-a0de45"
        obj = Place(id=idd, created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(obj.id, idd)
        self.assertEqual(obj.created_at, dt)
        self.assertEqual(obj.updated_at, dt)
    
class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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
        obj = Place()
        sleep(0.05)
        first_updated_at = obj.updated_at
        obj.save()
        second_updated_at = obj.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        obj.save()
        self.assertLess(second_updated_at, obj.updated_at)

    def test_save_with_error_arg(self):
        obj = Place()
        with self.assertRaises(TypeError):
            obj.save(None)

    def test_save_storage_file(self):
        obj = Place()
        obj.save()
        bmid = "Place." + obj.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())
    


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        bm = Place()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        obj = Place()
        self.assertIn("id", obj.to_dict())
        self.assertIn("created_at", obj.to_dict())
        self.assertIn("updated_at", obj.to_dict())
        self.assertIn("__class__", obj.to_dict())

    def test_to_dict_contains_added_attributes(self):
        obj = Place()
        obj.name = "alx"
        obj.my_number = 777
        self.assertIn("name", obj.to_dict())
        self.assertIn("my_number", obj.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        obj = Place()
        obj_dict = obj.to_dict()
        self.assertEqual(str, type(obj_dict["created_at"]))
        self.assertEqual(str, type(obj_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        obj = Place()
        obj.id = "123456"
        obj.created_at = obj.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(obj.to_dict(), tdict)

    

    def test_to_dict_with_error_arg(self):
        obj = Place()
        with self.assertRaises(TypeError):
            obj.to_dict(None)


if __name__ == "__main__":
    unittest.main()
