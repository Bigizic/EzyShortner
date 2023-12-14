#!/usr/bin/python3
"""Function that renders user's information page
@param (user_id): <str> from session['user_id'], in uuid.uuid4() format
"""

import bcrypt
from flask import render_template, current_app
from models.ezy import Ezy
from models.users import User
from models.engine.db_storage import DBStorage
import uuid


def infopage(user_id, sec_info=None, first_info=None):
    """Renders information.html"""
    info = DBStorage().fetch_user(user_id)
    if info:
        names = info.first_name + ' ' + info.last_name
        email = info.email[:2].upper()
        full_email = info.email
        if sec_info:
            return render_template('user_routes/information.html',
                                   cache_id=uuid.uuid4(), names=names,
                                   email=email, user_id=user_id,
                                   full_email=full_email, sec_info=sec_info)
        elif first_info:
            return render_template('user_routes/information.html',
                                   cache_id=uuid.uuid4(), names=names,
                                   email=email, user_id=user_id,
                                   full_email=full_email, info=first_info)
        else:
            return render_template('user_routes/information.html',
                                   cache_id=uuid.uuid4(), names=names,
                                   email=email, user_id=user_id,
                                   full_email=full_email,
                                   sec_info="Successfully Changed")

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
        full_email = info.email
    else:
        return render_template('signin.html', info="Oops.. No user Found",
                               cache_id=uuid.uuid4())

    # checks in user_info dict for credentials that match updated info
    if user_info:
        # names
        f_name = user_info.get('first_name')
        l_name = user_info.get('last_name')

        if f_name and not l_name:
            if len(f_name) >= 127:
                return infopage(user_id, None, "Oops.. too long")

            new_first_name = DBStorage().update_user(user_id, f_name)
            return infopage(user_id)

        if l_name and not f_name:
            if len(l_name) >= 127:
                return infopage(user_id, None, "Oops.. too long")

            new_last_name = DBStorage().update_user(user_id, None, l_name)
            return infopage(user_id)

        if l_name and f_name:
            if len(f_name) >= 127 or len(l_name) >= 127:
                return infopage(user_id, None, "Oops.. too long")

            new_names = DBStorage().update_user(user_id, f_name, l_name)
            return infopage(user_id)

        # password
        o_pass = user_info.get('old_password')
        n_pass = user_info.get('new_password')

        if o_pass and n_pass:
            if (len(o_pass) >= 127 or len(n_pass) >= 127 or
                    len(o_pass) <= 7 or len(n_pass) <= 7):
                return infopage(user_id, None, "Password length must be >= 8")

        user = DBStorage().fetch_user(user_id)
        if user and o_pass and n_pass:
            old_pass = user.password
            compare_old = bcrypt.checkpw(o_pass.encode(), old_pass.encode())
            if compare_old:
                # replace old password with new one
                DBStorage().update_user(user_id, None, None, n_pass)
                return infopage(user_id, sec_info="Successfully Changed!!")
            else:
                return infopage(user_id, None, "Invalid details")

    return render_template('user_routes/information.html',
                           cache_id=uuid.uuid4(), email=email, names=names,
                           user_id=user_id, full_email=full_email)
