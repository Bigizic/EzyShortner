#!/usr/bin/python3
"""
Account information module about a user like login time and logout time
"""

import bcrypt
from models.Ezy_model import EzyModel, Base
import pyotp
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Table, JSON
from sqlalchemy.orm import relationship
import uuid


class AccountInformation(EzyModel, Base):
    """Implementation
    """
    __tablename__ = "account_information"
    user_id = Column(String(100), unique=True, nullable=True)

    login_time = Column(JSON, nullable=True)

    logout_time = Column(JSON, nullable=True)
