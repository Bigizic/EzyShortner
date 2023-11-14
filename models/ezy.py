#!/usr/bin/python3
"""A class that sets the parameters needed and add other funtionality
basically the entry point
"""


import datetime
import uuid
import models
import requests
from requests.exceptions import ConnectionError, TooManyRedirects
from requests.exceptions import MissingSchema, RequestException, Timeout
from shortner.url_shortner import url_shortner
from shortner.url_shortner import generate_random_url
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
BASEURL = "ezyurl.xyz/"


class Ezy(Base):
    """default storage: MySql db"""

    __tablename__ = "records"

    id = Column(String(100), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    original_url = Column(String(2000), nullable=False)
    short_url = Column(String(70), nullable=False)

    def __init__(self, *args, **kwargs):
        """Sets the default parameters for database"""
        short = False
        if kwargs:
            for k, v in kwargs.items():
                if k == "original_url":
                    setattr(self, k, v)
                if k == "short_url":
                    short = True
                    setattr(self, k, v)

        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()

        if not kwargs:
            self.original_url = "NOPE NO URL"

        # self.short_url = url_shortner(self.original_url)
        if not short:
            self.short_url = url_shortner(self.original_url)

    def to_dict(self):
        """Creates a dictionary representation of the instance
        """
        my_dict = self.__dict__.copy()
        my_dict['created_at'] = my_dict['created_at'].strftime(
                "%Y-%m-%dT%H:%M:%S.%f")

        del my_dict['_sa_instance_state']
        return my_dict

    def __str__(self):
        """Handels string representation of the class
        basically the print()
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Writes information about the `Ezy` instance to the database
        """
        models.storage_type.new(self)
        models.storage_type.save()

    def remove_url(self):
        """Remove the instanced Url from the database"""
        models.storage_type.delete(self)

    def exists(self, alias=None):
        """Makes a call to the database existing() to check if the
        short_url exists in the database
        """
        if alias:
            return models.storage_type.existing(None, alias)

        if not alias and models.storage_type.existing(self.short_url) is True:
            self.short_url = generate_random_url()

    def url(self):
        """returns the shortned url plus the subdomain
        """
        return BASEURL + self.short_url
