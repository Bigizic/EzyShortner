#!/usr/bin/pytohn3
"""Web app using flask"""

import bcrypt
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests as g_req
from flask import g
from flask import Flask, request, render_template, make_response, session
from flask import Blueprint, redirect, url_for, current_app
from models import storage_type as st
from models.account_information import AccountInformation as ACCI
from models.ezy import Ezy
from models.users import GoogleUser, EzyUser
from models.engine.db_storage import DBStorage
from os import environ
from shortner.qr_img_gen import qr_gen
from app.web_app_functions import alias
from app.web_app_functions.application import application
from app.web_app_functions.dashpage import dashpage
from app.web_app_functions.homepage import homepage
from app.web_app_functions.historypage import historypage
from app.web_app_functions.information import information
from app.web_app_functions.editlink import editlink
from app.routes.signup.google_signup import google_signup
from app.routes.signup.ezy_signup import ezy_signup
from app.routes.signin.ezy_signin import ezy_signin
from app.routes.signin.google_signin import google_signin
from typing import Union
import pyotp
import re
import uuid
import logging
import random
import string

TIME = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
web_app_blueprint = Blueprint('web_app', __name__)
CLIENT_ID = ('518132922807-8vsde0i71v5nktavtssmt1j8vtugvu6o'
             '.apps.googleusercontent.com')
CID = uuid.uuid4()


def check_session() -> bool:
    """Checks session data to see if a user's logged in
    """
    if ('logged_in' in session and session['logged_in'] and
            session.get('user_id')):
        return True
    else:
        return False


@web_app_blueprint.route("/", methods=["GET", "POST"])
def get_input() -> Union[render_template, homepage]:
    if check_session():
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))

    if request.method == "POST":
        user_input = request.form.get("user_input")
        user_output = request.form.get("user_output")
        res = application(user_input, user_output)
        return homepage(res[0], res[1], res[2], res[3], res[4])
    return render_template('homepage.html', cache_id=CID)


@web_app_blueprint.route('/about')
def about() -> render_template:
    """Renders static/about page"""
    return render_template('about.html', cache_id=CID)


@web_app_blueprint.route('/signup', methods=["GET", "POST"])
def sign_up() -> Union[render_template, redirect, google_signup, ezy_signup]:
    """Renders sign up page"""
    if check_session():
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))

    if request.method == 'POST':
        # google sign up
        if request.form.get('credential'):
            return google_signup(request)
        # ezy sign up
        if request.form.get("email"):
            return ezy_signup(request)

    info_message = session.pop('info_message', None)
    return render_template('signup.html', info=info_message,
                           cache_id=CID)


@web_app_blueprint.route('/signin', methods=["GET", "POST"])
def sign_in() -> Union[render_template, redirect, google_signin, ezy_signin]:
    """Renders sign in page"""
    if check_session():
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))

    if request.method == 'POST':
        if request.form.get('credential'):
            return google_signin(request)

        if request.form.get('email'):
            return ezy_signin(request)

    info_message = session.pop('info_message', None)
    return render_template('signin.html', cache_id=CID, info=info_message)


@web_app_blueprint.route('/dashboard/<user_id>', methods=["GET", "POST"],
                         strict_slashes=False)
def dashboard(user_id: str) -> Union[dashpage, render_template, redirect]:
    """User's dashboard

    Parameters:
        - @param (user_id): <str> user id from database
    """
    if request.method == "POST":
        user_input = request.form.get("user_input")
        user_output = request.form.get("user_output")
        res = application(user_input, user_output, user_id)
        return dashpage(res[0], res[1], res[2], res[3], res[4])

    if check_session():
        g_user = GoogleUser().exists(None, None, user_id)
        e_user = EzyUser().exists(None, None, user_id)
        if g_user or e_user:
            info = DBStorage().fetch_user(user_id)
            names = info.first_name + ' ' + info.last_name
            profile_pic = info.profile_pic
            return render_template('dashboard.html', cache_id=CID,
                                   names=names, profile_pic=profile_pic,
                                   user_id=session.get('user_id'))
        else:
            # direct a user if they've been blocked to sign in
            session['logged_in'] = False
            session['info_message'] = "Account doesn't exist"
            return redirect(url_for('web_app.sign_in'))
    else:
        session['logged_in'] = False
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/dashboard', methods=["GET", "POST"])
def dashboard_helper() -> redirect:
    """Incase a user enters a route like server_name/dashboard
    Redirects them to the original dashboard route
    """
    if check_session():
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/history/<user_id>', methods=["GET", "POST"])
def history(user_id: str) -> Union[historypage, redirect]:
    """Renders history for a user
    Parameters:
        - @param (user_id): <str> User's id from database
    """
    if request.method == "POST":
        query = request.form.get("query")
        return historypage(user_id, query)

    if check_session():
        return historypage(user_id)

    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/history', methods=["GET", "POST"])
def history_helper() -> redirect:
    """Incase a user enters a route like server_name/history
    redirects user to the history route
    """
    if check_session():
        return redirect(url_for('web_app.history',
                        user_id=session['user_id']))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/history/delete/<ezy_url_id>',
                         methods=["POST"])
def delete_history(ezy_url_id: str) -> redirect:
    """Deletes an instance of a url
    Parameter:
        - @param (ezy_url_id): <str> id of the created shortened link,
            in __tablename__ >>>> link_records
    """
    if check_session():
        g_user = GoogleUser().exists(None, None, session.get('user_id'))
        e_user = EzyUser().exists(None, None, session.get('user_id'))
        if g_user or e_user:
            st.delete(None, ezy_url_id)
            return redirect(url_for('web_app.history',
                            user_id=session['user_id']))
        else:
            session['info_message'] = "Sign in to continue"
            return redirect(url_for('web_app.sign_in'))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/profile/<user_id>',
                         methods=["GET", "POST"])
def user_profile(user_id: str) -> Union[information, redirect,
                                        render_template]:
    """ Render user's profile information

    Parameter:
        - @param (user_id): <str> User id from database
    """
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        old_pass = request.form.get("old_password")
        new_pass = request.form.get("new_password")

        del_pass = request.form.get("del_old_password")

        user_credentials = {
                'first_name': first_name,
                'last_name': last_name,
                'old_password': old_pass,
                'new_password': new_pass
        }
        otp_list = [request.form.get('digit-1'),
                    request.form.get('digit-2'),
                    request.form.get('digit-3'),
                    request.form.get('digit-4'),
                    request.form.get('digit-5'),
                    request.form.get('digit-6')]
        # delete a user bassed on del_pass passed from client
        if del_pass:
            temp_user = st.fetch_user(user_id)
            compare_old = bcrypt.checkpw(del_pass.encode(),
                                         temp_user.password.encode())
            uak = temp_user.two_factor
            su = pyotp.totp.TOTP(uak).provisioning_uri(
                                 name=temp_user.first_name,
                                 issuer_name='https://ezyurl.xyz')
            if compare_old:
                st.delete(None, None, user_id)
                session.clear()
                session['info_message'] = "Successfully deleted!!"
                return redirect(url_for('web_app.sign_in'))
            else:
                return render_template('user_routes/information.html',
                                       cache_id=CID, info=temp_user,
                                       user_id=user_id,
                                       first_info="Check your entries",
                                       qr_authy=su)

        return information(user_id, user_credentials,
                           otp_list if None not in otp_list else None)

    if check_session():
        return information(user_id)
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/profile/delete/<ezy_url_id>',
                         methods=["POST"])
def delete_profile(ezy_url_id: str) -> redirect:
    """Deletes a user profile
    Parameter:
        - @param {ezy_url_id}: id of a shortened link from database
    """
    if check_session():
        g_user = GoogleUser().exists(None, None, session.get('user_id'))
        e_user = EzyUser().exists(None, None, session.get('user_id'))
        if g_user or e_user:
            st.delete(None, None, ezy_url_id)
            session.clear()
            session['info_message'] = "Successfully deleted!!"
            return redirect(url_for('web_app.sign_in'))
        else:
            session['info_message'] = "Sign in to continue"
            return redirect(url_for('web_app.sign_in'))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/edit-my-links/<user_id>', methods=["GET", "POST"])
def edit_my_link(user_id: str) -> Union[redirect, editlink]:
    """Edits a user's long link
    Parameter:
        - @param {user_id}: user id of logged in user
    """
    if request.method == "POST":
        long_link = request.form.get("long_link")
        short = request.form.get("short_link")
        query = request.form.get("query")
        if query:
            return editlink(user_id, None, query)
        if long_link and short:
            return editlink(user_id, [long_link, short], None)

    if check_session():
        return editlink(user_id)
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/verify_user', methods=["GET", "POST"])
def verify_user() -> Union[redirect, render_template]:
    """Verifies a user if they set up extra layer of security
    """
    if check_session():
        return redirect(url_for('web_app.dashboard'))

    if request.method == "POST":
        otp_list = [request.form.get('digit-1'),
                    request.form.get('digit-2'),
                    request.form.get('digit-3'),
                    request.form.get('digit-4'),
                    request.form.get('digit-5'),
                    request.form.get('digit-6')]

        otps = ''
        count = 0
        for _ in range(6):
            otps += otp_list[count]
            count += 1

        fetch_user = st.fetch_user(session.get("user_id"))
        if fetch_user:
            two_fa = fetch_user.two_factor
            totp = pyotp.TOTP(two_fa)
            totp.now()
            verified = totp.verify(otps)
            if verified:
                session["logged_in"] = True
                return redirect(url_for("web_app.dashboard",
                                user_id=session.get("user_id")))
            else:
                return render_template('user_routes/verify_user.html',
                                       cache_id=CID,
                                       info="Check your entries")
    if session.get('user_id'):
        wor = "Enter otp from authenticator app to continue"
        return render_template('user_routes/verify_user.html',
                               cache_id=CID,
                               info=wor)
    session['info_message'] = "Sign in to continue"
    return redirect(url_for("web_app.sign_in"))


@web_app_blueprint.route('/logout', methods=["GET"])
def logout() -> redirect:
    """clear the session data"""
    if not session.get('user_id'):
        session['info_message'] = "Sign in to continue"
        return redirect(url_for("web_app.sign_in"))
    u_id = session.get('user_id')

    fetch = st.fetch_account_info(u_id)
    if fetch:
        st.update_account_info(u_id, None, 'logout')

    session.clear()
    return redirect(url_for('web_app.get_input'))


@web_app_blueprint.route('/<shortlink>')
def redirect_function(shortlink) -> Union[render_template, make_response]:
    """Perfroms redirection refain to redirection.txt"""
    url = Ezy().get_long(shortlink)

    if url is not None:
        if not url.startswith("https://") and not url.startswith("http://"):
            url = 'http://' + url

        response = make_response('')
        response.headers['Location'] = url
        response.status_code = 302
        return response
    else:
        return render_template('/errors/404.html', cache_id=CID,
                               code=404)
