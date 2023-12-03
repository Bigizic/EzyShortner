#!/usr/bin/python3


import bcrypt
from models.ezy import Ezy
from models.users import User
from models import storage_type
import unittest


class TestUser(unittest.TestCase):
    """ Begin testing user class """

    def test_user_creation(self):
        """Tests user creation"""
        t = User()
        t.email = "goat@gmail.com"
        t.first_name = "goat"
        t.last_name = "ora"
        t.password = "sdfdsfsd"
        t.save()
        self.assertTrue(storage_type.fetch_user(t.id))

    def test_user_linked_with_long_url(self):
        """ Test user creation and user linked with an original_url """
        t = User()
        t.email = "somethuing@gmaisv.vodsvnds"
        t.first_name = "girl"
        t.last_name = "boy"
        t.password = "ergdfgdfgdf"
        t_id = t.id
        t.save()

        ins = Ezy()
        ins.original_url = "ssword_in_bycrpt example.com"
        ins.user_id = t_id
        ins.save()
        self.assertTrue(storage_type.fetch_user_and_ezy(t_id))

    def test_verify_user_password_in_bycrpyt_format(self):
        """ Checks if the user password is saved in bycrpyt format """
        t = User()
        t.email = "something@yahoo.com"
        t.first_name = "yui"
        t.last_name = "something"
        t.password = "verify"
        t.save()

        # fetch user by email from database
        fetch = storage_type.fetch_user(None, t.email)
        is_bcrypt = (bcrypt.checkpw("verify".encode('utf-8'),
                     fetch.password.encode('utf-8')))
        assert is_bcrypt, "Password is not in bcrypt format"
