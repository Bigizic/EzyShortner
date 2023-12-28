#!/usr/bin/python3
"""function that handle's a user post request to edit
a long link to a short link
@param (link): <list> contains long link and short link
@prarm (qury): <str> contains search query

Return: template
"""

from flask import render_template, current_app
from models import storage_type as st
from models.ezy import Ezy
from models.users import EzyUser, GoogleUser
from models.engine.db_storage import DBStorage
import re
import uuid


def editpage(user_id, info=None, sec_info=None):
    """ Implementation """
    g_user = GoogleUser().exists(None, None, user_id)
    e_user = EzyUser().exists(None, None, user_id)
    if g_user or e_user:
        fe_user = st.fetch_user(user_id)
        names = fe_user.first_name + ' ' + fe_user.last_name
        profile_pic = fe_user.profile_pic
        his = st.fetch_user_and_ezy(user_id)
        if his:
            history = sorted(his, key=lambda x: x['created_at'], reverse=True)
        else:
            history = ''

        return render_template('user_routes/edit.html',
                               cache_id=uuid.uuid4(),
                               names=names, user_id=user_id,
                               profile_pic=profile_pic,
                               history_items=history,
                               info=info if info else sec_info)
    else:
        session['info_message'] = "Account doesn't exist"
        return redirect(url_for('web_app.sign_in'))


def editlink(user_id, links=None, query=None):
    """ Implementation """
    if links:
        edit_record = st.update_user_longL_record(user_id, links[0], links[1])
        if edit_record:
            return editpage(user_id, "Successfully updated")
        else:
            return editpage(user_id, None, "Check your entries")

    if query:
        long_result = st.search(user_id, query)

        query = re.search(r'[^/]+$', query)

        short_result = st.search(user_id, None, query[0])

        result = long_result if long_result else short_result

        g_user = GoogleUser().exists(None, None, user_id)
        e_user = EzyUser().exists(None, None, user_id)

        user = g_user if g_user else e_user
        info = st.fetch_user(user_id)
        names = info.first_name + ' ' + info.last_name
        profile_pic = info.profile_pic

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
            return render_template('user_routes/edit.html',
                                   cache_id=uuid.uuid4(),
                                   names=names, user_id=user_id,
                                   profile_pic=profile_pic,
                                   history_items=search_result)
        else:
            return render_template('user_routes/edit.html', names=names,
                                   cache_id=uuid.uuid4(),
                                   profile_pic=profile_pic,
                                   user_id=user_id, info="NO RESULTS")

    g_user = GoogleUser().exists(None, None, user_id)
    e_user = EzyUser().exists(None, None, user_id)
    if g_user or e_user:
        info = st.fetch_user(user_id)
        names = info.first_name + ' ' + info.last_name
        profile_pic = info.profile_pic
        his = st.fetch_user_and_ezy(user_id)
        if his:
            history = sorted(his, key=lambda x: x['created_at'],
                             reverse=True)
        else:
            history = ''
        return render_template('user_routes/edit.html',
                               cache_id=uuid.uuid4(), names=names,
                               profile_pic=profile_pic,
                               user_id=user_id,
                               history_items=history)
    else:
        # direct a user if they've been blocked to sign in
        session['info_message'] = "Account doesn't exist"
        return redirect(url_for('web_app.sign_in'))
