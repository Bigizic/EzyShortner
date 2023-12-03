#!/usr/bin/pytohn3
"""Web app using flask"""

from flask import Flask, request, render_template, make_response, session
from models.ezy import Ezy
from models.users import User
from models.engine.db_storage import DBStorage
from os import environ
from shortner.qr_img_gen import qr_gen
import uuid
from app.web_app_routes import web_app_blueprint
import logging


# app = Flask(__name__, static_folder='static', static_url_path='/static')
app = Flask(__name__)
app.secret_key = environ.get("FLASK_KEY")
app.url_map.strict_slashes = False

if not app.debug:
    app.logger.setLevel(logging.INFO)


@app.before_request
def before_request():
    """ Initialize logged_in status in session """
    session.setdefault('logged_in', False)

app.register_blueprint(web_app_blueprint)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)