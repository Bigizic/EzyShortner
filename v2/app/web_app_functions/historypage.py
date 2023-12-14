#!/usr/bin/python3
"""Function that render's user's history page
@param (user_id): <str> from session['user_id'] also in uuid.uuid4() format
@param (query): <str> search query, default=None

Return: history template
"""

from flask import render_template, current_app
from models.ezy import Ezy
from models.users import User
from models.engine.db_storage import DBStorage
import re
import uuid


def historypage(user_id, query=None):
    """Renders the history page returns crucial info"""
    if query:
        long_result = DBStorage().search(user_id, query)

        query = re.search(r'[^/]+$', query)

        short_result = DBStorage().search(user_id, None, query[0])

        result = long_result if long_result else short_result

        user = User().exists(None, None, user_id)
        info = DBStorage().fetch_user(user_id)
        names = info.first_name + ' ' + info.last_name
        email = info.email[:2].upper()

        if result:
            sear = []
            for obj in result:
                cl_name = type(obj).__name__
                id = obj.id
                attr = {k: v for k, v in obj.__dict__.items()
                        if not k.startswith('_sa_instance_state')}

                sear.append({
                    **attr
                })
            search_result = sorted(sear, key=lambda x: x['created_at'],
                                   reverse=True)
            # search result successful
            return render_template('user_routes/history.html',
                                   cache_id=uuid.uuid4(),
                                   email=email, names=names,
                                   user_id=user_id,
                                   history_items=search_result)
        else:
            return render_template('user_routes/history.html',
                                   cache_id=uuid.uuid4(),
                                   email=email, names=names,
                                   user_id=user_id,
                                   info="NO RESULTS")

    user = User().exists(None, None, user_id)
    if user:
        info = DBStorage().fetch_user(user_id)
        names = info.first_name + ' ' + info.last_name
        email = info.email[:2].upper()
        his = DBStorage().fetch_user_and_ezy(user_id)
        if his:
            history = sorted(his, key=lambda x: x['created_at'],
                             reverse=True)
        else:
            history = ''
        return render_template('user_routes/history.html',
                               cache_id=uuid.uuid4(),
                               email=email, names=names,
                               user_id=user_id,
                               history_items=history)
    else:
        # direct a user if they've been blocked to sign in
        session['info_message'] = "Account doesn't exist"
        return redirect(url_for('web_app.sign_in'))
