#!/usr/bin/python3
"""Function that renders user's information page
"""

import bcrypt
from flask import render_template, current_app
from models import storage_type as st
from models.ezy import Ezy
from models.users import EzyUser, GoogleUser
from models.engine.db_storage import DBStorage
from typing import List, Union
import uuid
import pyotp

EZY = 'https://ezyurl.xyz'


def infopage(user_id: str, sec_info: str = None, first_info: str = None,
             otp_list: List[int] = None) -> render_template:
    """Renders information.html, a helper function that renders the html based
        on certain warnings, credentials etc..

    parameters:
        - @param (user_id): <str> from session['user_id'], uuid.uuid4() format

        - @param (sec_info): <str> Second info usually flashed in green
            color on user page

        - @param (first_info): <str> First info usually warning info and
            in red color

        - @param (otp_list): <list> a list of 6 numbers from user
    """
    info = st.fetch_user(user_id)
    if info:
        # sets and show user 2fa
        uak = info.two_factor
        su = pyotp.totp.TOTP(uak).provisioning_uri(name=info.first_name,
                                                   issuer_name=EZY)
        if sec_info:
            return render_template('user_routes/information.html',
                                   cache_id=uuid.uuid4(), info=info,
                                   user_id=user_id, sec_info=sec_info,
                                   qr_authy=su)
        elif first_info:
            return render_template('user_routes/information.html',
                                   cache_id=uuid.uuid4(), info=info,
                                   user_id=user_id, first_info=first_info,
                                   qr_authy=su)
        elif otp_list:
            # verify user enterd otp
            otps = ''
            count = 0
            for _ in range(6):
                otps += otp_list[count]
                count += 1

            totp = pyotp.TOTP(info.two_factor)
            totp.now()
            verified = totp.verify(otps)
            if verified:
                # user enetered otp is valid
                # procced to update user "two_factor_status" record to enabled
                st.update_user(user_id, None, None, None, 'enabled')
                info = st.fetch_user(user_id)  # fetch new user details
                return render_template('user_routes/information.html',
                                       cache_id=uuid.uuid4(),
                                       user_id=user_id,
                                       info=info, sec_info='Enabled!!',
                                       qr_authy=su)
            else:
                iop = 'check your entries'
                return render_template('user_routes/information.html',
                                       cache_id=uuid.uuid4(),
                                       user_id=user_id, first_info=iop,
                                       info=info, qr_authy=su)

        else:
            return render_template('user_routes/information.html',
                                   cache_id=uuid.uuid4(), user_id=user_id,
                                   info=info, sec_info="Successfully Changed",
                                   qr_authy=su)

    else:
        return render_template('signin.html',
                               first_info="Oops.. No user Found",
                               cache_id=uuid.uuid4())


def information(user_id: str, user_info: str = None,
                otp_list: List[int] = None) -> Union[render_template,
                                                     infopage]:
    """ If a user's request is post, allows editing user names, password
    and enabling 2fa otherwise render's user information page

    Parameters:
        - @param (user_id): <str> from session['user_id'], uuid.uuid4() format
        - @param (user_infor): <str> Warning information for user
        - @param (otp_list): <list> list of 6 digit numbers
    """
    g_user = GoogleUser().exists(None, None, user_id)
    e_user = EzyUser().exists(None, None, user_id)
    if g_user or e_user:
        info = st.fetch_user(user_id)
    else:
        return render_template('signin.html',
                               first_info="Oops.. No user Found",
                               cache_id=uuid.uuid4())

    if otp_list is not None:
        return infopage(user_id, None, None, otp_list)

    # checks in user_info dict for credentials that match updated info
    if user_info:
        # names
        f_name = user_info.get('first_name')
        l_name = user_info.get('last_name')

        if f_name and not l_name:
            if len(f_name) >= 127:
                return infopage(user_id, None, "Oops.. too long")

            new_first_name = st.update_user(user_id, f_name)
            return infopage(user_id)

        if l_name and not f_name:
            if len(l_name) >= 127:
                return infopage(user_id, None, "Oops.. too long")

            new_last_name = st.update_user(user_id, None, l_name)
            return infopage(user_id)

        if l_name and f_name:
            if len(f_name) >= 127 or len(l_name) >= 127:
                return infopage(user_id, None, "Oops.. too long")

            new_names = st.update_user(user_id, f_name, l_name)
            return infopage(user_id)

        # password
        o_pass = user_info.get('old_password')
        n_pass = user_info.get('new_password')

        if o_pass and n_pass:
            if (len(o_pass) >= 127 or len(n_pass) >= 127 or
                    len(o_pass) <= 7 or len(n_pass) <= 7):
                return infopage(user_id, None, "Password length must be >= 8")

        if info and o_pass and n_pass:
            old_pass = info.password
            compare_old = bcrypt.checkpw(o_pass.encode(), old_pass.encode())
            if compare_old:
                # replace old password with new one
                st.update_user(user_id, None, None, n_pass)
                return infopage(user_id, sec_info="Successfully Changed!!")
            else:
                return infopage(user_id, None, "Invalid details")

    uak = info.two_factor
    su = pyotp.totp.TOTP(uak).provisioning_uri(name=info.first_name,
                                               issuer_name=EZY)

    return render_template('user_routes/information.html',
                           cache_id=uuid.uuid4(), user_id=user_id,
                           info=info, qr_authy=su)
