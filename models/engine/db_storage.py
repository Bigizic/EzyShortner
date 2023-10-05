#!/usr/bin/python3
"""Prepares the database connector and engine"""


import models
from os import environ
from models.ezy import Ezy, Base
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    __session = None
    __engine = None

    def __init__(self):
        """Creates a connection"""
        USER = environ.get("EZYUSER")
        PWD = environ.get("EZYPWD")
        HST = "0.0.0.0"
        DB = "Ezy_url"
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(USER, PWD, HST, DB))
        self.reload()

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def all(self):
        """Query all records of the current database session
        Returns a dictionary of all records"""
        result = {}
        objs = self.__session.query(Ezy).all()
        for items in objs:
            key = items.__class__.__name__ + '.' + item.id
            result[key] = items
        return result

    def save(self):
        """Save/commit all changes of the current session"""
        self.__session.commit()

    def new(self, session):
        """Adds new object to the current database"""
        self.__session.add(session)

    def delete(self):
        """Deletes the current session record if it's not None"""
        self.__session.delete()

    def close(self):
        """Close the current session"""
        self.__session.remove()

    def get(self, id):
        """Given an id of the instance it'll return the object based on it's id
        otherwise return None"""
        result = None
        if id:
            result = self.__session.query(Ezy).filter_by(id=id).first()
        return result

    def count(self):
        """Returns number of records in the database"""
        result = 0
        result += self.__session.query(Ezy).count()
        return result

    def existing(self, my_short_url):
        """This function reloads data from the database and checks
        if the {short_url} column has any records of the shortened
        url
        Returns:
            True if it exists otherwise false
        """
        if my_short_url:
            exists = self.__session.query(Ezy).filter_by(
                    short_url=my_short_url).first()
        return True if exists is not None else False
