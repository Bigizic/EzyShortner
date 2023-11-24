#!/usr/bin/pytohn3
"""Web app using flask"""

import bcrypt
from flask import Flask, request, render_template, make_response, session
from flask import Blueprint, redirect, url_for, current_app
from models.ezy import Ezy
from models.users import User
from models.engine.db_storage import DBStorage
from os import environ
from shortner.qr_img_gen import qr_gen
import uuid
import logging


web_app_blueprint = Blueprint('web_app', __name__)


@web_app_blueprint.route("/", methods=["GET", "POST"])
def get_input():
    if "logged_in" in session and session['logged_in']:
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))

    if request.method == "POST":
        user_input = request.form.get("user_input")

        if user_input.startswith(('https://ezyurl.xyz/', 'ezyurl.xyz/',
                                  'http://ezyurl.xyz/',
                                  'https://www.ezyurl.xyz/',
                                  'http://www.ezyurl.xyz/')):
            return homepage('', '', 404, '', 'Cannot use Domain')
        user_output = request.form.get("user_output")

        wor = "Long link enterd is not a valid address"
        alias_error = "Alias has been used please try another"

        ezy_instance = Ezy()
        ezy_instance.original_url = user_input

        if user_output:
            bad_alias = ["api", "api/", "api//", "api-docs", "api/docs/",
                         "api_docs", "signup", "signup/docs", "sign_up",
                         "sign-up", "signin", "signin/docs", "sign_in",
                         "sign-in", "aboutus", "about", "about_us",
                         "about-us", "dashboard", "dash_board",
                         "dash-board", "dashboard/", "dashboard//",
                         "dashboard_"]

            if user_output in bad_alias or len(user_output) > 70:
                return homepage('', '', 404, '', 'Oops... Not Allowd')

            ezy_instance.short_url = user_output

            alias = func_alias(ezy_instance, user_output)
            if alias == "alias exist original url valid":
                """This would check if the alias exists before saving
                and if the original url entered by user is valid"""
                # ezy_instance.remove_url()  # deletes the created instance
                ezy_instance.save()
                return homepage('', 404, '', alias_error, '')

            ezy_instance.save()
            if alias == "alias exist original url invalid":
                ezy_instance.remove_url()  # deletes the created instance
                return homepage('', 404, '', '', wor)
            if alias == "alias doesn't exist original url invalid":
                ezy_instance.remove_url()  # deletes the created instance
                return homepage('', 404, '', '', wor)
            if alias == "alias doesn't exist original url valid":
                short_url = ezy_instance.url()
                qr_file_path = qr_gen(short_url)
                return homepage('https://' + short_url, 200,
                                qr_file_path, '', '')
        else:
            ezy_instance.exists()  # check for existence before saving
            ezy_instance.save()
            if ezy_instance.url():
                short_url = ezy_instance.url()
                qr_file_path = qr_gen(short_url)
                return homepage('https://' + short_url, 200,
                                qr_file_path, '', '')
            else:
                return homepage('', 404, '', '', wor)
    return render_template('homepage.html', cache_id=uuid.uuid4())


def homepage(short_url, status_code, qr_file_path, alias, word):
    """Renders homepage"""
    return render_template('homepage.html', url=short_url,
                           status=status_code, qr_image=qr_file_path,
                           alias_status=alias, word=word,
                           cache_id=uuid.uuid4())


def func_alias(ezy_instance, user_output):
    """Handles:
    ALIAS EXIST ORIGINAL URL INVALID
                |
    Return: (str) "alias exist original url invalid"
    ALIAS EXIST ORIGINAL URL VALID
                |
    Return: (str) "alias exist original url valid"

    ALIAS DOESN'T EXIST ORIGINAL URL INVALID
                |
    Return: (str) "alias doesn't exist original url invalid"
    ALIAS DOESN'T EXIST ORIGINAL URL VALID
                |
    Return: (str) "alias doesn't exist original url valid"
    """
    alias = ezy_instance.exists(user_output)
    valid_url = ezy_instance.url()

    if alias and not valid_url:
        return "alias exist original url invalid"
    if alias and valid_url:
        return "alias exist original url valid"

    if not alias and not valid_url:
        return "alias doesn't exist original url invalid"
    if not alias and valid_url:
        return "alias doesn't exist original url valid"


@web_app_blueprint.route('/about')
def about():
    """Renders static/about page"""
    return render_template('about.html', cache_id=uuid.uuid4())


@web_app_blueprint.route('/signup', methods=["GET", "POST"])
def sign_up():
    """Renders sign up page"""
    if request.method == 'POST':
        email = request.form.get("email")
        # protect against attacks
        if len(email) > 128 or not email.find('@') or email is None:
            return render_template('signup.html', info="email is invalid!",
                                   cache_id=uuid.uuid4())
        password = request.form.get("pass")
        if len(password) > 128 or password is None:
            ps = "Oops.. check the password"
            return render_template('signin.html', info=ps,                           
                                   cache_id=uuid.uuid4())

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        new_user = User()
        new_user.email = email
        new_user.password = password
        new_user.first_name = first_name
        new_user.last_name = last_name
        if new_user.exists(None, email):
            return render_template('signup.html', info="email already exits!",
                                   cache_id=uuid.uuid4())
        new_user.save()
        session['user_email'] = email
        session['logged_in'] = True
        session['user_id'] = new_user.id
        return redirect(url_for("web_app.dashboard", user_id=new_user.id))

    info_message = session.pop('info_message', None)
    return render_template('signup.html', info=info_message,
                           cache_id=uuid.uuid4())


@web_app_blueprint.route('/signin', methods=["GET", "POST"])
def sign_in():
    """Renders sign in page"""
    if "logged_in" in session and session['logged_in']:
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))

    if request.method == 'POST':
        email = request.form.get("email")
        # protect against attacks
        if len(email) > 128 or not email.find('@') or email is None:
            return render_template('signin.html', info="email is invalid!",
                                   cache_id=uuid.uuid4())
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

        if user_id and user_pass:
            # compares html password and database password
            passs = bcrypt.checkpw(password.encode(), user_pass.encode())
            if passs:
                session['logged_in'] = True
                session['email'] = email
                session['user_id'] = user_id
                return redirect(url_for("web_app.dashboard", user_id=user_id))
            else:
                return render_template('signin.html',
                                       info="Oops wrong password",
                                       cache_id=uuid.uuid4())

    info_message = session.pop('info_message', None)
    return render_template('signin.html', cache_id=uuid.uuid4())


@web_app_blueprint.route('/dashboard/<user_id>', methods=["GET", "POST"],
                         strict_slashes=False)
def dashboard(user_id):
    if ('logged_in' in session and session['logged_in'] and
            session['user_id'] == user_id):
        user = User().exists(None, None, user_id)
        if user:
            return render_template('dashboard.html', cache_id=uuid.uuid4())
        else:
            # direct a user if they've been blocked to sign in
            session['info_message'] = "Account doesn't exist"
            return redirect(url_for('web_app.sign_in'))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/dashboard', methods=["GET", "POST"])
def dashboard_helper():
    """Incase a user enters a route like server_name/dashboard"""
    if ('logged_in' in session and session['logged_in']):
        return redirect(url_for('web_app.dashboard',
                        user_id=session['user_id']))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/logout', methods=["GET"])
def logout():
    """clear the session data"""
    session.clear()
    return redirect(url_for('web_app.get_input'))


"""Perfroms redirection
HOW IT WORKS:
A user accesses a short URL like ezyurl.com/shortlink in their web browser
Nginx Receives the Request
Nginx Routes the Request to Python Script
Nginx is configured to route all incoming requests to a specific location
Nginx sends the request to this Python script for processing.
The URL path, /shortlink is passed as part of the request to the Python script
The script looks up the original URL associated with shortlink from database
If it finds a matching original URL, it creates a redirection response.
it generates an HTTP redirection response using a 302 status code.
Nginx receives the HTTP redirection response from the Python script.
Nginx processes the redirection response and performs the redirection
based on the Location header. It tells the user's web browser to navigate
to the original URL.
"""


@web_app_blueprint.route('/<shortlink>')
def redirect_function(shortlink):
    """Perfroms redirection"""
    result = DBStorage()
    url = result.redirect(shortlink)

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
