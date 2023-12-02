#!/usr/bin/python3
"""A class that sets the parameters needed and add other funtionality
basically the entry point
"""


import datetime
import uuid
import models
from models.Ezy_model import EzyModel, Base
import requests
from requests.exceptions import ConnectionError, TooManyRedirects
from requests.exceptions import MissingSchema, RequestException, Timeout
from shortner.url_shortner import url_shortner
from shortner.url_shortner import generate_random_url
import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import re

BASEURL = "ezyurl.xyz/"


class Ezy(EzyModel, Base):
    """default storage: MySql db"""

    __tablename__ = "records"
    original_url = Column(String(32000), nullable=False)
    short_url = Column(String(70), nullable=False)
    user_id = Column(String(100), ForeignKey('users.id'))
    clicks = Column(BigInteger, nullable=True, default=0)

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super().__init__(*args, **kwargs)

    def url(self):
        """returns the shortned url plus the subdomain
        """
        link = self.original_url
        if len(link) > 2:
            pattern = r'^(https?://|www\.)'
            sec = r'\.\w+'
            if re.match(pattern, link) or re.search(sec, link):
                return BASEURL + self.short_url
            else:
                return None
