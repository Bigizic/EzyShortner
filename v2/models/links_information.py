#!/usr/bin/python3
"""Handles user links information
foreign key users and user_id
"""

import bcrypt
from models.Ezy_model import EzyModel, Base
import pyotp
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Table
from sqlalchemy.orm import relationship
import uuid
from flask import current_app


class LinksInformation(EzyModel, Base):
    """LinksInformation class implementation
    """

    __tablename__ = 'links_information'

    def __init__(self, *args, **kwargs):
        """Constructor
        """
