#!/usr/bin/python3
"""
Admin
"""

import bcrypt
from datetime import datetime
from models.Ezy_model import EzyModel, Base
import pyotp
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Table, JSON
from sqlalchemy.orm import relationship
import uuid
from flask import current_app


class Admin(EzyModel, Base):
    """ Decleration of user """
    __tablename__ = 'admin'
    username = Column(String(128), nullable=False, unique=True)

    password = Column(String(255), nullable=False)

    full_name = Column(String(300), nullable=False)

    login_time = Column(JSON, default=str(datetime.utcnow()), nullable=False)

    logout_time = Column(JSON, nullable=True)

    two_factor = Column(String(50), nullable=False)  # 2 factor authy

    # 2 factor status
    two_factor_status = Column(String(15), default="enabled")

    rights = Column(String, default="GET")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, attribute, value):
        """Set the user's password securely before it's saved in
        the database"""
        secrets = ["password", "username"]
        if attribute in secrets:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(value.encode(), salt).decode()
            super().__setattr__(attribute, hashed_password)
        else:
            super().__setattr__(attribute, value)
