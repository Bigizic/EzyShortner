#!/usr/bin/python3
"""
Contains the Tests to DBSTORAGE methods.
"""

import models
from os import environ
from models.ezy import Ezy, Base
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import unittest
from models.ezy import Ezy
from models import storage_type
from sqlalchemy.orm.session import Session
import pep8


class TestDBStorageMethods(unittest.TestCase):
    """This class contains all Database methods tests"""

    def test_db_storage_pass_pep8(self):
        """Tests for pycodestyle"""
        codestyle = pep8.StyleGuide(quiet=True)
        res = codestyle.check_files(['./models/engine/db_storage.py'])
        self.assertEqual(res.total_errors, 0, "Found code style error")

    def test_db_storage_test_pass_pep8(self):
        """Test if this test file pass pycodestyle"""
        codestyle = pep8.StyleGuide(quiet=True)
        res = codestyle.check_files(
                    ['tests/test_database/test_db_storage.py'])
        self.assertEqual(res.total_errors, 0, "Found code style error")

    def test_new(self):
        """Test if new() method create a session or not"""
        ins = Ezy()
        ins.original_url = "mywebsite.com"
        storage_type.new(ins)
        storage = list(storage_type._DBStorage__session.new)
        self.assertIn(ins, storage)

    def test_save(self):
        """Test if save() method saves the data in the database"""
        ins = Ezy()
        ins.original_url = "not-mywebsite.com"
        num = storage_type.count()
        storage_type._DBStorage__session.add(ins)
        storage_type.save()
        sec_num = storage_type.count()

        self.assertNotEqual(num, sec_num)
        self.assertEqual(num + 1, sec_num)
        storage_type._DBStorage__session.commit()

    def test_delete(self):
        """Test if delete() method deletes a data from database"""
        ins = Ezy()
        ins.original_url = "this-mywebsite.com"
        storage_type._DBStorage__session.add(ins)
        """Here delete() method deletes and commits the changes to the
        database by itself"""
        storage_type.delete(ins)
        deleted_objects = list(storage_type._DBStorage__session.deleted)

        """Verify that delete() method commited chnges"""
        self.assertEqual(len(deleted_objects), 0)

        storage_type._DBStorage__session.commit()

        self.assertNotIn(ins, deleted_objects)

    def test_count(self):
        """Test if count() method returns number of instance"""
        ins = Ezy()
        ins.original_url = "No-mywebsite.com"
        storage_type._DBStorage__session.add(ins)
        storage_type._DBStorage__session.commit()
        num = storage_type.count()

        self.assertTrue(num)  # returns True if num is not None

        ins_two = Ezy()
        ins_two.original_url = "Two-No-mywebsite.com"
        storage_type._DBStorage__session.add(ins_two)
        storage_type._DBStorage__session.commit()

        num_two = storage_type.count()
        self.assertEqual(num + 1, num_two)
        self.assertNotEqual(num, num_two)

    def test_reload(self):
        """Test if reload() method reloads the data from the database"""
        sess = storage_type._DBStorage__session
        storage_type.reload()
        self.assertNotIsInstance(storage_type._DBStorage__session, Session)
        self.assertNotEqual(sess, storage_type._DBStorage__session)
        storage_type._DBStorage__session.close()
        storage_type._DBStorage__session = sess

    def test_existing(self):
        """Test existing() method"""
        ins = Ezy()
        ins.original_url = "three-mywebsite.com"
        storage_type._DBStorage__session.add(ins)
        storage_type._DBStorage__session.commit()
        self.assertTrue(storage_type.existing(ins.short_url))

    def test_existing_alias(self):
        """Test existing() method alias parameter"""
        ins = Ezy()
        ins.original_url = "four-mywebsite.com"
        ins.short_url = "myshortmanisagoat"
        storage_type._DBStorage__session.add(ins)
        storage_type._DBStorage__session.commit()

        two = Ezy()
        two.original_url = "five-mywebsite.com"
        two.short_url = ins.short_url
        storage_type._DBStorage__session.add(two)
        storage_type._DBStorage__session.commit()

        self.assertEqual(storage_type.existing(None, two.short_url),
                         "Alias has been used please try another")

    def test_redirect(self):
        """Tests redirect() method"""
        inst = Ezy()
        inst.original_url = "six-mywebsite.com"
        inst.short_url = "potatoes.com/sdgf"
        storage_type._DBStorage__session.add(inst)
        storage_type._DBStorage__session.commit()

        self.assertEqual(storage_type.redirect(inst.short_url),
                         inst.original_url)

    def test_all(self):
        """Tests all() method"""
        insta = Ezy()
        insta.original_url = "seven-mywebsite.com"
        storage_type._DBStorage__session.add(insta)
        storage_type._DBStorage__session.commit()
        res = storage_type.all(insta.original_url)

        self.assertEqual(type(res), list)
        for _ in res:
            self.assertEqual(type(_), dict)
            self.assertTrue(_.get("title"))
            self.assertTrue(_.get("id"))
            self.assertTrue(_.get("created_at"))
            self.assertTrue(_.get("short_url"))

    def test_all_short_link(self):
        """Test all() method short_link"""
        instan = Ezy()
        instan.original_url = "Eight-mywebsite.com"
        storage_type._DBStorage__session.add(instan)
        storage_type._DBStorage__session.commit()
        res = storage_type.all(instan.short_url)

        self.assertEqual(type(res), list)
        for _ in res:
            self.assertEqual(type(_), dict)
            self.assertTrue(_.get("title"))
            self.assertTrue(_.get("id"))
            self.assertTrue(_.get("created_at"))
            self.assertTrue(_.get("short_url"))


if __name__ == '__main__':
    unittests.main()
