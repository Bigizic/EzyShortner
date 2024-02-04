#!/usr/bin/python3
"""Admin app using flask"""

import bcrypt
from datetime import timedelta
from flask import Flask, request, render_template, session, flash, g
from flask import Blueprint, redirect, url_for, current_app
# from models.engine.admin_storage import AdminStorage as AS
# from models.admin import Admin
from os import environ
import uuid
import logging
import random

app = Flask(__name__)
app.secret_key = environ.get("ADMIN_KEY")
app.url_map.strict_slashes = False
hashed = b'$2b$12$OHXRZbf5.2WsSeEUFQmQLuG71EYNufwJDd2521eNA5Y/88S/b8Q7u'


@app.before_request
def handler() -> None:
    """handles admin session
    """
    session.setdefault('logged_in', False)


def admin_session() -> bool:
    """handles admin session """
    if session.get('admin_id') and 'logged_in' in session and \
        session['logged_in']:
            return True
    return False


@app.route("/admin/welcome", methods=["GET", "POST"])
def admin_welcome():
    """Login page for admin
    """
    if admin_session():
        return redirect(url_for('app.admin_dashboard', session['admin_id']))

    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_pass = request.form.get("password")
        #return redirect(url_for('app.logged_in', g.username))
    return render_template('/admin/welcome.html')

@app.route('/admin/dashboard/<admin_id>', methods=['GET', 'POST'])
def admin_dashboard(admin_id: str):
    """Admin dashboard """
    if admin_session():
        pass



if __name__ == "__main__":
    password = environ.get("ADMIN_KEY")
    if not bcrypt.checkpw(password.encode(), hashed):
        print("TRY AGAIN")
        exit(0)
    app.run(host='0.0.0.0', port=1738)
