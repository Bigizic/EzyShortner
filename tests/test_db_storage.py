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
from models.engine import db_storage
from models.ezy import Ezy
from models import storage_type
from sqlalchemy.orm.session import Session

class TestDBStorageMethods(unittest.TestCase):
    """This class contains all methods' tests"""
    def test_new(self):
        """testing if new create a session or not"""
        ins = Ezy()
        self.storage_type.new(ins)
        storage = list(self.storage_type._DBStorage__session.new)
        self.assertIn(ins, storage)

    def test_save(self):
        """Test if it save the data in the database or not"""
        ins = Ezy()
        self.storage_type._DBStorage__session.add(ins)
        self.storage_type.save()
        num = self.storage_type._DBStorage__session.count()
        self.assertEqual(num, 1)

    def test_delete(self):
        """Test if it delete the data from database or not"""
        ins = Ezy()
        self.storage_type._DBStorage__session.add(ins)
        self.storage_type._DBStorage__session.commit()
        self.storage_type.delete(ins)
        self.assertIn(ins, list(self.storage_type._DBStorage__session.deleted))

    def test_count(self):
        """Test if it returns number of instance or not"""
        ins = Ezy()
        self.storage_type._DBStorage__session.add(ins)
        self.storage_type._DBStorage__session.commit()
        num = self.storage_type.count()
        self.assertEqual(num, 1)
        ins = Ezy()
        self.storage_type._DBStorage__session.add(ins)
        self.storage_type._DBStorage__session.commit()
        num = self.storage_type.count()
        self.assertEqual(num, 2)

    def test_reload(self):
        """Test if it reloads the data from the database or not"""
        sess = self.storage_type._DBStorage__session
        self.storage_type.reload()
        self.assertIsInstance(self.storage_type._DBStorage__session, Session)
        self.assertNotEqual(sess, self.storage._DBStorage__session)
        self.storage_type._DBStorage__session.close()
        self.storage_type._DBStorage__session = sess

    def test_existing(self):
        """Test if it checks the data is in the database or not"""
        ins = Ezy()
        self.storage_type._DBStorage__session.add(ins)
        self.storage_type._DBStorage__session.commit()
        self.assertTrue(self.storage_type._DBStorage__session.existing(ins))
