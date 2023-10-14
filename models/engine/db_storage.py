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

    def all(self, long_link=None, short_link=None):
        """Query all records of the current database session
        Returns a dictionary of all records of a link"""
        objs = []
        result = {}
        if long_link:
            objs += self.__session.query(Ezy).filter_by(
                        original_url=long_link).all()

        if short_link:
            objs = self.__session.query(Ezy).filter_by(
                        short_url=short_link).first()

            attr = {k: v for k, v in objs.__dict__.items()
                    if not k.startswith('_sa_instance_state')}

            result[f'[{type(objs).__name__}].({objs.id})'] = {**attr}
            return result

        for obj in objs:
            cl_name = type(obj).__name__
            id = obj.id
            attr = {k: v for k, v in obj.__dict__.items()
                    if not k.startswith('_sa_instance_state')}

            result[f'[{cl_name}].({id})'] = {**attr}
        return result

    def save(self):
        """Save/commit all changes of the current session"""
        self.__session.commit()

    def new(self, session):
        """Adds new object to the current database"""
        self.__session.add(session)

    def delete(self, ins=None):
        """Deletes the current session record if it's not None"""
        if ins is not None:
            self.__session.delete(ins)
            self.__session.commit()
        else:
            pass

    def close(self):
        """Close the current session"""
        self.__session.remove()

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
