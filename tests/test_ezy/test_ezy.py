#!/usr/bin/python3
"""Unittests for Ezy class and methods
"""

import unittest
import pep8
from models.ezy import Ezy
import datetime
from models import storage_type


class TestEzyCodeStyle(unittest.TestCase):

    def test_ezy_pass_pep8(self):
        """Tests for pycodestyle"""
        codestyle = pep8.StyleGuide(quiet=True)
        res = codestyle.check_files(['./models/ezy.py'])
        self.assertEqual(res.total_errors, 0, "Found code style error")

    def test_ezy_test_pass_pep8(self):
        """Test if this test file pass pycodestyle"""
        codestyle = pep8.StyleGuide(quiet=True)
        res = codestyle.check_files(['tests/test_ezy/test_ezy.py'])
        self.assertEqual(res.total_errors, 0, "Found code style error")


class TestEzyToDict(unittest.TestCase):
    """Tests for to dict method"""

    def test_ezy_to_dict_method(self):
        """Test ezy class to dict method"""
        ins = Ezy()
        ins.original_url = "www.google.com"
        res = ins.to_dict()
        self.assertEqual(type(res), dict, "Not a dictionary")
        self.assertTrue(res.get("short_url"))

    def test_to_dict_returns(self):
        """Test if to_dict returns what's supposed to"""
        ins = Ezy()
        ins.original_url = "www.google.com"
        res = ins.to_dict()
        self.assertFalse(res.get("_sa_instance_state"))
        self.assertNotIn(res.get("_sa_instance_state"), res)
        self.assertTrue((type(res.get("created_at")), datetime))
        self.assertTrue(res.get("id"))
        self.assertTrue(res.get("created_at"))

    def test_to_dict_attribute_types(self):
        """Test short_url of to_dict"""
        ins = Ezy()
        ins.original_url = "google.com"
        ins.short_url = "datetime-police"
        res = ins.to_dict()
        self.assertEqual(res.get("short_url"), "datetime-police")

    def test_to_dict_original_url_types(self):
        """Test if the original_url accepts certain types"""
        types = [None, True, False, 3.142, 34, "34", "sharon"]
        ins = Ezy()
        for _ in types:
            ins.original_url = _
            res = ins.to_dict()
            self.assertIn("id", res)
            self.assertEqual(res.get("original_url"), _)


class TestEzySaveMethod(unittest.TestCase):

    def test_save(self):
        """Test if the save() method automatically save an
        ezy object when it's called upon
        """
        ins = Ezy()
        ins.original_url = "dgdfgerteyeryreb.com"
        ins.save()
        self.assertTrue(storage_type.all(ins.original_url))

    def test_save_retrieve_attributes(self):
        """Test if specific attributes can be retrieved from the
        database after saving them
        """
        ins = Ezy()
        ins.original_url = "erwerwerwrw.com"
        ins.save()
        obj = storage_type.all(ins.original_url)
        self.assertEqual(type(obj), list)
        for _ in obj:
            self.assertTrue(_.get("original_url"))
            self.assertTrue(_.get("id"))
            self.assertTrue(_.get("created_at"))
            self.assertTrue(_.get("short_url"))


class TestEzyRemove_Url(unittest.TestCase):

    def test_remove_url(self):
        """Test if the remove_url would not delete an
        object that's not saved in the database
        """
        ins = Ezy()
        ins.original_url = "yusdafasfas.com"
        self.assertEqual(ins.remove_url(), None)

    def test_save_then_remove_url(self):
        """Test if the remove_url deletes an object that's
        saved in the database
        """
        ins = Ezy()
        ins.original_url = "wefwsfsdfdscsc.com"
        ins.save()
        obj = storage_type.all(ins.original_url)
        self.assertTrue(obj)
        self.assertEqual(type(obj), list)
        ins.remove_url()
        objs = storage_type.all(ins.original_url)
        self.assertFalse(objs)
        self.assertEqual(len(objs), 0)


class TestExistsMethod(unittest.TestCase):

    def test_exists_returns_none(self):
        """Test to see if a short_url doesn't exist
        """
        ins = Ezy()
        res = ins.exists("https://ezyurl.tech/mycook.com/dfgdfg")
        self.assertEqual(res, False)
