#!/usr/bin/python3
""" Creation of user class """


import bcrypt
from models.Ezy_model import EzyModel, Base
import sqlalchemy
from sqlalchemy import Column, String
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
