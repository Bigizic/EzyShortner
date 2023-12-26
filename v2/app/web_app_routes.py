#!/usr/bin/pytohn3
"""Web app using flask"""

import bcrypt
from google.oauth2 import id_token
from google.auth.transport import requests as g_req
from flask import Flask, request, render_template, make_response, session
from flask import Blueprint, redirect, url_for, current_app
from models.ezy import Ezy
from models.users import User
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
import pyotp
import re
import uuid
import logging

web_app_blueprint = Blueprint('web_app', __name__)
CLIENT_ID = '518132922807-8vsde0i71v5nktavtssmt1j8vtugvu6o.apps.googleusercontent.com'


def check_session():
    """Checks session data to see if a user's logged in
    """
    if ('logged_in' in session and session['logged_in'] and
            session['user_id']):
        return True
    else:
        return False


@web_app_blueprint.route("/", methods=["GET", "POST"])
def get_input():
    if check_session():
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))

    if request.method == "POST":
        user_input = request.form.get("user_input")
        user_output = request.form.get("user_output")
        res = application(user_input, user_output)
        return homepage(res[0], res[1], res[2], res[3], res[4])
    return render_template('homepage.html', cache_id=uuid.uuid4())


@web_app_blueprint.route('/about')
def about():
    """Renders static/about page"""
    return render_template('about.html', cache_id=uuid.uuid4())


@web_app_blueprint.route('/signup', methods=["GET", "POST"])
def sign_up():
    """Renders sign up page"""
    if check_session():
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))

    if request.method == 'POST':
        if request.form.get('credential'):
            try:
                token = request.form.get('credential')
                idinfo = id_token.verify_oauth2_token(token,
                                                      g_req.Request(),
                                                      CLIENT_ID)
                if idinfo:
                    email = idinfo.get('email')
                    first_name = idinfo.get('given_name')
                    last_name = idinfo.get('family_name')
                    verified = idinfo.get('email_verified')
                    google_id = idinfo.get("sub")  # for google id
                    account_creation = 'google'
                    password = None
            except ValueError:
                return render_template('signup.html',
                                       info="Invalid account!",
                                       cache_id=uuid.uuid4())
        if request.form.get("email"):   
            email = request.form.get("email")
            # protect against attacks
            if len(email) > 128 or not email.find('@') or email is None:
                return render_template('signup.html',
                                       info="email is invalid!",
                                       cache_id=uuid.uuid4())
            account_creation = None
            password = request.form.get("pass")
            if len(password) > 128 or password is None:
                ps = "Oops.. check the password"
                return render_template('signup.html', info=ps,
                                       cache_id=uuid.uuid4())

            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")

            if len(first_name) >= 127 or len(last_name) >= 127:
                return render_template('signup.html',
                                       info="names too long",
                                       cache_id=uuid.uuid4())

        new_user = User()
        new_user.email = email
        if password is not None:
            new_user.password = password
        new_user.first_name = first_name
        new_user.last_name = last_name

        new_user.Two_factor = pyotp.random_base32()

        if account_creation is not None:
            new_user.verified = verified
            new_user.google_id = google_id
            new_user.authentication_method = 'google'

            if new_user.exists(None, None, None, google_id):
                return render_template('signup.html',
                                        info="user already exits!",
                                        cache_id=uuid.uuid4())

        if new_user.exists(None, email) and not account_creation:
            return render_template('signup.html', info="email already exits!",
                                   cache_id=uuid.uuid4())
        new_user.save()
        session['user_email'] = email
        session['logged_in'] = True
        session['user_id'] = new_user.id
        session.permanent = True
        return redirect(url_for("web_app.dashboard", user_id=new_user.id))

    info_message = session.pop('info_message', None)
    return render_template('signup.html', info=info_message,
                           cache_id=uuid.uuid4())


@web_app_blueprint.route('/signin', methods=["GET", "POST"])
def sign_in():
    """Renders sign in page"""
    if check_session():
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))

    if request.method == 'POST':
        if request.form.get('credential'):
            try:
                token = request.form.get('credential')
                idinfo = id_token.verify_oauth2_token(token,
                                                      g_req.Request(),
                                                      CLIENT_ID)
                if idinfo:
                    email = idinfo.get('email')
                    google_id = idinfo.get("sub")  # for google id
                    password = None
            except ValueError:
                return render_template('signin.html',
                                       info="Invalid account!",
                                       cache_id=uuid.uuid4())
        if request.form.get('email'):
            email = request.form.get("email")
            # protect against attacks
            if len(email) > 128 or not email.find('@') or email is None:
                return render_template('signin.html',
                                       info="email is invalid!",
                                       cache_id=uuid.uuid4())
            google_id = None
            password = request.form.get("pass")
            if len(password) > 128 or password is None:
                ps = "Oops.. check the password"
                return render_template('signin.html', info=ps,
                                       cache_id=uuid.uuid4())

        # check for existence of user via email return id and password
        user_data = DBStorage().existing(None, None, email)
        if not user_data:
            return render_template('signin.html', info="Oops.. No user Found",
                                   cache_id=uuid.uuid4())
        user_id, user_pass = user_data if user_data else None

        if google_id is not None:
            session['logged_in'] = True
            session['email'] = email
            session['user_id'] = user_id
            session.permanet = True
            return redirect(url_for("web_app.dashboard", user_id=user_id))

        if user_id and user_pass:
            # compares html password and database password
            passs = bcrypt.checkpw(password.encode(), user_pass.encode())
            if passs:
                session['logged_in'] = True
                session['email'] = email
                session['user_id'] = user_id
                session.permanent = True
                return redirect(url_for("web_app.dashboard", user_id=user_id))
            else:
                return render_template('signin.html',
                                       info="Oops wrong information",
                                       cache_id=uuid.uuid4())

    info_message = session.pop('info_message', None)
    return render_template('signin.html', cache_id=uuid.uuid4(),
                           info=info_message)


@web_app_blueprint.route('/dashboard/<user_id>', methods=["GET", "POST"],
                         strict_slashes=False)
def dashboard(user_id):
    """User's dashboard"""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        user_output = request.form.get("user_output")
        res = application(user_input, user_output, user_id)
        return dashpage(res[0], res[1], res[2], res[3], res[4])

    if check_session():
        user = User().exists(None, None, user_id)
        if user:
            info = DBStorage().fetch_user(user_id)
            names = info.first_name + ' ' + info.last_name
            email = info.email[:2].upper()
            return render_template('dashboard.html', cache_id=uuid.uuid4(),
                                   names=names, email=email,
                                   user_id=session['user_id'])
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
def dashboard_helper():
    """Incase a user enters a route like server_name/dashboard"""
    if check_session():
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/history/<user_id>', methods=["GET", "POST"])
def history(user_id):
    """Renders history for a user"""
    if request.method == "POST":
        query = request.form.get("query")
        return historypage(user_id, query)

    if check_session():
        return historypage(user_id)

    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/history', methods=["GET", "POST"])
def history_helper():
    """Incase a user enters a route like server_name/history"""
    if check_session():
        return redirect(url_for('web_app.history',
                        user_id=session['user_id']))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/history/delete/<ezy_url_id>',
                         methods=["POST"])
def delete_history(ezy_url_id):
    """Deletes an instance of a url"""
    if check_session():
        user = User().exists(None, None, session['user_id'])
        if user:
            DBStorage().delete(None, ezy_url_id)
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
def user_profile(user_id):
    """ Render user's profile information """
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        old_pass = request.form.get("old_password")
        new_pass = request.form.get("new_password")
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
                    request.form.get('digit-6')
        ]
        return information(user_id, user_credentials,
                otp_list if None not in otp_list else None)

    if check_session():
        return information(user_id)
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/profile/delete/<ezy_url_id>',
                         methods=["POST"])
def delete_profile(ezy_url_id):
    """Deletes a user profile"""
    if check_session():
        user = User().exists(None, None, session.get('user_id'))
        if user:
            DBStorage().delete(None, None, ezy_url_id)
            session['info_message'] = "Successfully deleted!!"
            session.clear()
            return redirect(url_for('web_app.sign_in'))
        else:
            session['info_message'] = "Sign in to continue"
            return redirect(url_for('web_app.sign_in'))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/edit-my-links/<user_id>', methods=["GET", "POST"])
def edit_my_link(user_id):
    """Edits a user's long link"""
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


@web_app_blueprint.route('/logout', methods=["GET"])
def logout():
    """clear the session data"""
    session.clear()
    return redirect(url_for('web_app.get_input'))


@web_app_blueprint.route('/<shortlink>')
def redirect_function(shortlink):
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
        return render_template('not_found.html', cache_id=uuid.uuid4(),
                               code=404)
