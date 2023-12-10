#!/usr/bin/python3
""" Creation of user class """


import bcrypt
from models.Ezy_model import EzyModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
import uuid


class User(EzyModel, Base):
    """ Decleration of user """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    ezy_urls = relationship("Ezy", backref="user")
    verified = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, attribute, value):
        """Set the user's password securely before it's saved in
        the database"""
        if attribute == "password":
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(value.encode(), salt).decode()
            super().__setattr__(attribute, hashed_password)
        else:
            super().__setattr__(attribute, value)

    def edit_details(self, user_id, DBStorage_ins, names=None, passW=None):
        """ Edit a userr's credential """
        # check for existence of user via email return id and password
        user = DBStorage_ins.fetch_user(user_id)
        if user:
            old_pass = user.password

        if names:
                DBStorage_ins.update_user(user_id, names[0], names[1], None)
                return True

        if passW:
            user_pass = passW[0]  # user entered password from browser
            compare_old = bcrypt.checkpw(old_pass.encode(), user_pass.encode())
            if compare_old:
                # replace old password with new one 
                DBStorage_ins.update_user(user_id, None, None, passW[1])
                return True

        return False
