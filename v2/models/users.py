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

    def set_password(self, password):
        """Set the user's password securely."""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, password):
        """Check if the provided password is correct."""
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
