#!/usr/bin/python3
"""Prepares the database connector and engine"""


import bcrypt
from flask import current_app
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

    def delete(self, ins=None, ezy_id=None):
        """Deletes the current session record if it's not None"""
        try:
            if ins is not None:
                self.__session.delete(ins)
                self.__session.commit()
            elif ezy_id is not None:
                self.__session.query(Ezy).filter_by(id=ezy_id).delete()
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
                 user_id=None, google_id=None):
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
                
            if google_id:
                exists = self.__session.query(User).filter_by(
                         google_id=google_id).first()
                return True if exists else False

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
        res = self.__session.query(Ezy).filter(
                                   Ezy.short_url == url).first()
        if res:
            res.clicks += 1  # stores in the database number of clicks
            self.__session.commit()
            return res.original_url
        else:
            return None

    def fetch_user_and_ezy(self, user_id):
        """checks in the database a user id and the
        user_id column of the records table if there's a match
        returns everything it can find on that user created objects
        """
        objs = []
        result = []
        objs += self.__session.query(Ezy).filter(
                                      Ezy.user_id == user_id).all()
        for obj in objs:
            cl_name = type(obj).__name__
            id = obj.id
            attr = {k: v for k, v in obj.__dict__.items()
                    if not k.startswith('_sa_instance_state')}

            result.append({
                **attr
            })
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

    def search(self, user_id=None, longl=None, short=None):
        """Query the database with the user's id to find a
        record of short link or long link associated with a user
        """
        user = self.__session.query(User).filter(
                                    User.id == user_id).first()
        if user:
            long_link = self.__session.query(Ezy).filter(
                                             Ezy.user_id == user_id,
                                             Ezy.original_url == longl).all()
            short_link = self.__session.query(Ezy).filter(
                                              Ezy.user_id == user_id,
                                              Ezy.short_url == short).all()
            if long_link:
                return long_link
            if short_link:
                return short_link
        return False

    def update_user(self, user_id, first_name=None, last_name=None,
                    new_password=None):
        """ Updates a user record """
        user = self.__session.query(User).filter(User.id == user_id).first()

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if new_password is not None:
            old_pass = user.password
            user.password = new_password

        self.__session.commit()
        return True

    def update_user_longL_record(self, user_id, longL, shortL):
        """ Works for the edit your link route to update a user
        record
        """
        result = self.search(user_id, None, shortL.split('/')[3])
        if result:
            for obj in result:
                setattr(obj, 'original_url', longL)

            self.__session.commit()
            return True

        return False
