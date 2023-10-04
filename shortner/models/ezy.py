#!/usr/bin/python3
"""A class that sets the parameters needed and add other funtionality
basically the entry point
"""


import datetime
import uuid
from shortner.url_shortner import url_shortner
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ezy(Base):
    """default storage: MySql db"""

    __tablename__ = "records"

    id = Column(String(100), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    original_url = Column(String(2000), nullable=False)
    short_url = Column(String(30), nullable=False)

    def __init__(self, original_url, storage_type):
        """Sets the default parameters for database"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()
        self.original_url = original_url
        self.short_url = url_shortner(original_url)
        self.storage_type = storage_type

    def to_dict(self):
        """Creates a dictionary representation of the instance
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "original_url": self.original_url,
            "short_url": self.short_url
        }

    def save(self, session):
        """Writes information about the `Ezy` instance to the database
        """
        self.storage_type.new(session)
        self.storage_type.save()

    def remove_url(self):
        """Remove the instanced Url from the database"""
        self.storage_type.delete(self)

def create_ezy_instance(original_url, storage_type):
    return Ezy(original_url, storage_type)
