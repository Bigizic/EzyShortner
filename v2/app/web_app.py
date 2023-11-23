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


app = Flask(__name__)
app.secret_key = environ.get("FLASK_KEY")
Logged_in = False

if not app.debug:
    app.logger.setLevel(logging.INFO)


# Initialize logged_in status in session
@app.before_request
def before_request():
    session.setdefault('logged_in', False)

app.register_blueprint(web_app_blueprint)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
