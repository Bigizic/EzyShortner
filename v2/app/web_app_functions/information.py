#!/usr/bin/python3
"""Function that renders user's information page
@param (user_id): <str> from session['user_id'], in uuid.uuid4() format
"""

from flask import render_template
from models.ezy import Ezy
from models.users import User
from models.engine.db_storage import DBStorage
import uuid


def infopage(user_id):
    """Renders information.html"""
    info = DBStorage().fetch_user(user_id)
    if info:
        names = info.first_name + ' ' + info.last_name
        email = info.email[:2].upper()
        return render_template('user_routes/information.html',
                               cache_id=uuid.uuid4(), names=names, email=email,
                               user_id=user_id)
    else:
        return render_template('signin.html', info="Oops.. No user Found",
                               cache_id=uuid.uuid4())


def information(user_id, user_info=None):
    """ If a user's request is post, allows editing user names and password
    otherwise render's user information page
    """
    user = User().exists(None, None, user_id)
    if user:
        info = DBStorage().fetch_user(user_id)
        names = info.first_name + ' ' + info.last_name
        email = info.email[:2].upper()
    else:
        return render_template('signin.html', info="Oops.. No user Found",
                               cache_id=uuid.uuid4())

    # checks in user_info dict for credentials that match updated info
    if user_info:
        # names
        sto = DBStorage()
        f_name = user_info.get('first_name')
        l_name = user_info.get('last_name')
        if f_name and not l_name:
            new_first_name = User().edit_details(user_id, sto, [f_name, None])
            return infopage(user_id)

        if l_name and not f_name:
            new_last_name = User().edit_details(user_id, sto, [None, l_name])
            return infopage(user_id)

        if l_name and f_name:
            new_names = User().edit_details(user_id, sto, [f_name, l_name])
            return infopage(user_id)

        # password
        o_pass = user_info.get('old_password')
        n_pass = user_info.get('new_password')
        if o_pass and n_pass:
            new_pass = User().edit_details(user_id, sto, None,
                                           [o_pass, n_pass])
            if new_pass:
                return infopage(user_id)
            else:
                render_template('user_routes/information.html',
                                cache_id=uuid.uuid4(), email=email,
                                names=names, user_id=user_id,
                                info="Invalid details")

    return render_template('user_routes/information.html',
                           cache_id=uuid.uuid4(), email=email, names=names,
                           user_id=user_id)
