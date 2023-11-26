#!/usr/bin/python3
"""Prepares the database connector and engine"""


import models
from os import environ
from models.Ezy_model import EzyModel, Base
from models.ezy import Ezy
from models.users import User
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
                                      format(USER, PWD, HST, DB),
                                      pool_pre_ping=True)
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
        result = []
        if long_link:
            objs += self.__session.query(Ezy).filter_by(
                        original_url=long_link).all()

        if short_link:
            objs = self.__session.query(Ezy).filter_by(
                        short_url=short_link).first()
            if objs:
                attr = {k: v for k, v in objs.__dict__.items()
                        if not k.startswith('_sa_instance_state')}

                result.append({
                    'title': f'[{type(objs).__name__}].({objs.id})',
                    **attr
                })
                return result
            else:
                return None

        for obj in objs:
            cl_name = type(obj).__name__
            id = obj.id
            attr = {k: v for k, v in obj.__dict__.items()
                    if not k.startswith('_sa_instance_state')}

            result.append({
                'title': f'[{cl_name}].({id})',
                **attr
            })
        return result

    def save(self):
        """Save/commit all changes of the current session"""
        self.__session.commit()

    def new(self, session):
        """Adds new object to the current database"""
        self.__session.add(session)

    def delete(self, ins=None):
        """Deletes the current session record if it's not None"""
        try:
            if ins is not None:
                self.__session.delete(ins)
                self.__session.commit()
            else:
                return None
        except sqlalchemy.exc.InvalidRequestError:
            return None

    def close(self):
        """Close the current session"""
        self.__session.remove()

    def count(self, long_link=None, short_link=None):
        """Returns number of records in the database"""
        result = 0
        if long_link:
            result += self.__session.query(Ezy).filter_by(
                    original_url=long_link).count()
        elif short_link:
            result += self.__session.query(Ezy).filter_by(
                    short_url=short_link).count()
        else:
            result += self.__session.query(Ezy).count()

        return result

    def existing(self, my_short_url, alias=None, user_email=None,
                 user_id=None):
        """This function reloads data from the database and checks
        if the {short_url} column has any records of the shortened
        url
        Returns:
            True if it exists otherwise false
        """
        try:
            if alias:
                word = "Alias has been used please try another"
                exists = self.__session.query(Ezy).filter_by(
                    short_url=alias).first()
                return word if exists else False

            if my_short_url:
                exists = self.__session.query(Ezy).filter_by(
                         short_url=my_short_url).first()
                return True if exists else False
            if user_email:
                exists = self.__session.query(User).filter_by(
                         email=user_email).first()
                return [exists.id, exists.password] if exists else None
            if user_id:
                exists = self.__session.query(User).filter_by(
                         id=user_id).first()
                return True if exists else False

        except Exception:
            self.__session.rollback()
            return False

        finally:
            self.__session.close()

    def redirect(self, url):
        """returns original_url from database of a short_url
        """
        res = self.__session.query(Ezy.original_url).filter(
                                   Ezy.short_url == url).first()
        res.clicks += 1  # stores in the database number of clicks
        self.__session.commit()
        return res.original_url if res else None

    def fetch_user_and_ezy(self, user_id):
        """checks in the database a user id and the
        user_id column of the records table if there's a match
        returns everything it can find on that user created objects
        """
        result = self.__session.query(Ezy).filter(
                                      Ezy.user_id == user_id).all()
        return result if result else None

    def fetch_user(self, id, email=None):
        """Fetches a user from the database by email or id
        """
        if id:
            result = self.__session.query(User).filter(User.id == id).first()
            return result if result else None
        if email:
            result = self.__session.query(User).filter(
                                          User.email == email).first()
            return result if result else None
