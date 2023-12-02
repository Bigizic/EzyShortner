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
import re
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

    if ('logged_in' in session and session['logged_in'] and
            session['user_id'] == user_id):
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
    if ('logged_in' in session and session['logged_in']):
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

    if ('logged_in' in session and session['logged_in'] and
            session['user_id'] == user_id):
        return historypage(user_id)

    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/history', methods=["GET", "POST"])
def history_helper():
    """Incase a user enters a route like server_name/history"""
    if ('logged_in' in session and session['logged_in']):
        return redirect(url_for('web_app.history',
                        user_id=session['user_id']))
    else:
        session['info_message'] = "Sign in to continue"
        return redirect(url_for('web_app.sign_in'))


@web_app_blueprint.route('/history/delete/<ezy_url_id>',
                         methods=["POST"])
def delete_history(ezy_url_id):
    """Deletes an instance of a url"""
    if ('logged_in' in session and session['logged_in'] and
            session['user_id']):
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

"""FUNCTIONS
"""

def application(user_input, user_output, user_id=None):
    if len(user_input) >= 32000:
        return '', '', 404, 'Link must not be greater than 32000', ''

    if user_input.startswith(('https://ezyurl.xyz/', 'ezyurl.xyz/',
                              'http://ezyurl.xyz/',
                              'https://www.ezyurl.xyz/',
                              'http://www.ezyurl.xyz/')):
        return '', '', 404, '', 'Cannot shorten Ezy Domain'

    wor = "Long link enterd is not a valid address"
    alias_error = "Alias has been used please try another"

    ezy_instance = Ezy()
    ezy_instance.original_url = user_input

    if user_id:
        ezy_instance.user_id = user_id

    if user_output:
        bad_alias = ["api", "api-docs", "api_docs", "signup", "sign_up",
                     "sign-up", "signin", "sign_in", "sign-in", "aboutus",
                     "about", "about_us","about-us", "dashboard",
                     "dash_board", "dash-board", "dashboard_", "ezy", "ezy.",
                     "ezy.com"]
        pattern = r'[/\\]'
        sec = r'\.\w+'

        if user_output in bad_alias or len(user_output) > 70:
            return '', '', 404, '', 'Oops... Not Allowd'

        ezy_instance.short_url = user_output
        alias = func_alias(ezy_instance, user_output)
        if alias == "alias exist original url valid":
            ezy_instance.remove_url()  # deletes the created instance
            return '', 404, '', alias_error, ''
        if alias == "alias exist original url invalid":
            ezy_instance.remove_url()  # deletes the created instance
            return '', 404, '', '', wor

        if alias == "alias doesn't exist original url invalid":
            ezy_instance.remove_url()  # deletes the created instance
            return '', 404, '', '', wor
        if alias == "alias doesn't exist original url valid":
            ezy_instance.save()
            short_url = ezy_instance.url()
            qr_file_path = qr_gen(short_url)
            return 'https://' + short_url, 200, qr_file_path, '', ''
    else:
        if ezy_instance.url():
            ezy_instance.exists()  # check for existence before saving
            ezy_instance.save()
            short_url = ezy_instance.url()
            qr_file_path = qr_gen(short_url)
            return 'https://' + short_url, 200, qr_file_path, '', ''
        else:
            return '', 404, '', '', wor

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

def dashpage(short_url, status_code, qr_file_path, alias, word):
    """Renders dashpage"""
    user = User().exists(None, None, session.get('user_id'))
    if user:
        info = DBStorage().fetch_user(session.get('user_id'))
        names = info.first_name + ' ' + info.last_name
        email = info.email[:2].upper()

    return render_template('dashboard.html', url=short_url,
                           status=status_code, qr_image=qr_file_path,
                           alias_status=alias, word=word,
                           cache_id=uuid.uuid4(), user_id=session['user_id'],
                           names=names, email=email)

def historypage(user_id, query=None):
    """Renders the history page returns crucial info"""
    if query:
        long_result = DBStorage().search(user_id, query)

        if len(query) > 10:
            query = query[-7:]
            short_result = DBStorage().search(user_id, None, query)

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
        history = sorted(his, key=lambda x: x['created_at'],
                         reverse=True)
        return render_template('user_routes/history.html',
                               cache_id=uuid.uuid4(),
                               email=email, names=names,
                               user_id=user_id,
                               history_items=history)
    else:
        # direct a user if they've been blocked to sign in
        session['info_message'] = "Account doesn't exist"
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
