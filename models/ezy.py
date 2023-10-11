#!/usr/bin/python3
"""A class that sets the parameters needed and add other funtionality
basically the entry point
"""


import datetime
import uuid
import models
from shortner.url_shortner import url_shortner
from shortner.url_shortner import generate_random_url
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ezy(Base):
    """default storage: MySql db"""

    __tablename__ = "records"

    id = Column(String(100), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    original_url = Column(String(2000), nullable=False)
    short_url = Column(String(30), nullable=False)

    def __init__(self, original_url):
        """Sets the default parameters for database"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.original_url = original_url
        self.short_url = url_shortner(original_url)

    def to_dict(self):
        """Creates a dictionary representation of the instance
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "original_url": self.original_url,
            "short_url": self.short_url
        }

    def save(self):
        """Writes information about the `Ezy` instance to the database
        """
        models.storage_type.new(self)
        models.storage_type.save()

    def remove_url(self):
        """Remove the instanced Url from the database"""
        models.storage_type.delete(self)

    def exists(self):
        """Makes a call to the database existing() to check if the
        short_url exists in the database
        """
        if models.storage_type.existing(self.short_url) is True:
            self.short_url = generate_random_url()

    def url(self):
        """returns the shortned url plus the subdomain
        """
        return "https://Ezyurl.tech/" + self.short_url
