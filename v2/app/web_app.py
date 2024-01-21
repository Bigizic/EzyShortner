#!/usr/bin/python3
"""Web app using flask"""

import bcrypt
from datetime import timedelta
from flask import Flask, request, render_template, session, g
from flask_session import Session
from os import environ
from shortner.qr_img_gen import qr_gen
import uuid
from app.web_app_routes import web_app_blueprint
import logging
import random


app = Flask(__name__)
app.config['SESSION_PERMANET'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_COOKIE_SECURE'] = True
app.secret_key = environ.get("FLASK_KEY")
app.url_map.strict_slashes = False


if not app.debug:
    app.logger.setLevel(logging.INFO)

"""def add_random(num):
    return num + random.randint(1, 9000)"""

# app.jinja_env.globals.update(add_random=add_random)
hashed = b'$2b$12$N4LWAaNVRQyr6Yz12kRrBedYbzf4RtWNwSmHI.vZTys3hgdROSmXe'


@app.before_request
def before_request() -> None:
    """ Initialize logged_in status in session
    """
    session.setdefault('logged_in', False)


@app.errorhandler(500)
def error_500(error):
    """Handles error 500"""
    return render_template('errors/all_error.html', error_code=500)


@app.errorhandler(405)
def error_405(error):
    """Handles method not allowd for the requested url """
    return render_template('errors/all_error.html', error_code=405)


@app.errorhandler(502)
def error_502(error):
    return render_template('errors/all_error.html', error_code=502)


app.register_blueprint(web_app_blueprint)


if __name__ == "__main__":
    password = environ.get("FLASK_KEY")
    if not bcrypt.checkpw(password.encode(), hashed):
        print("TRY AGAIN")
        exit(0)
    app.run(host='0.0.0.0', port=5000)
