#!/usr/bin/python3
"""Function that render's a user dashpage
"""

from models.ezy import Ezy
from models.users import EzyUser, GoogleUser
from models.engine.db_storage import DBStorage
from flask import render_template, session
import uuid


def dashpage(short_url: str, status_code: int, qr_file_path: str,
             alias: str, word: str) -> render_template:
    """Renders dashpage
    Parameter:
        - @param (short_url): <str> client result,
            i.e shortened link e.g ezyurl.xyz/sdfdfks

        - @param (status_code): <int> A status code that allows the display of
            the qr image and other functionalities on user page,
            either 404 or 200

        - @param (qr_file_path): <str> file path to where user qr image is
            stored on machine

        - @param (alias): <str> User entered alias

        - @param (word): <str> warning message
    """
    g_user = GoogleUser().exists(None, None, session.get('user_id'))
    e_user = EzyUser().exists(None, None, session.get('user_id'))
    if g_user or e_user:
        info = DBStorage().fetch_user(session.get('user_id'))
        names = info.first_name + ' ' + info.last_name
        profile_pic = info.profile_pic

    return render_template('dashboard.html', url=short_url,
                           status=status_code, qr_image=qr_file_path,
                           alias_status=alias, word=word,
                           cache_id=uuid.uuid4(), user_id=session['user_id'],
                           names=names, profile_pic=profile_pic)
