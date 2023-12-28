#!/usr/bin/python3
"""
Holds information for users that created account with email and password
"""

import bcrypt
from models.Ezy_model import EzyModel, Base
import pyotp
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Table
from sqlalchemy.orm import relationship
import uuid
from flask import current_app


class EzyUser(EzyModel, Base):
    """ Decleration of user """
    __tablename__ = 'ezy_users'
    email = Column(String(128), nullable=False, unique=True)

    password = Column(String(255), nullable=False)

    first_name = Column(String(128), nullable=True)

    last_name = Column(String(128), nullable=True)

    verified = Column(String(20), default='No')  # email verification

    two_factor = Column(String(50), nullable=False)  # 2 factor authy

    # 2 factor status
    two_factor_status = Column(String(15), default="disabled")

    profile_pic = Column(String(5), default="N/A", nullable=False)

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


class GoogleUser(EzyModel, Base):
    """ Decleration of user """
    __tablename__ = 'google_users'
    google_id = Column(String(200), nullable=False, unique=True)

    email = Column(String(128), nullable=False, unique=True)

    first_name = Column(String(128), nullable=True)

    last_name = Column(String(128), nullable=True)

    verified = Column(String(20), default='No')  # email verification

    # 2 factor authentication
    two_factor = Column(String(50), nullable=False)

    # 2 factor status
    two_factor_status = Column(String(15), default="disabled")

    profile_pic = Column(String(200), default="N/A", nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
