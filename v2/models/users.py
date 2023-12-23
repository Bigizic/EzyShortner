#!/usr/bin/python3
""" Creation of user class """


import bcrypt
from models.Ezy_model import EzyModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Table
from sqlalchemy.orm import relationship
import uuid
from flask import current_app


class User(EzyModel, Base):
    """ Decleration of user """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    ezy_urls = relationship("Ezy", backref="user")
    verified = Column(String(20), default='No')  # email verification
    Two_factor = Column(String(20), default='disabled')  # 2 factor authy
    # for normal account creations or google account creation
    authentication_method = Column(String(20), default='Ezy')

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
