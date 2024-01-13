#!/usr/bin/python3
""" Admin model
"""


from datetime import datetime
import uuid
import models
import requests
from requests.exceptions import ConnectionError, TooManyRedirects
from requests.exceptions import MissingSchema, RequestException, Timeout
from shortner.url_shortner import url_shortner
from shortner.url_shortner import generate_random_url
import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
BASEURL = "ezyurl.xyz/"


class EzyModel(Base):

    __abstract__ = True

    id = Column(String(100), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
