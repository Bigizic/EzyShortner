#!/usr/bin/python3
"""Renders Google users sign in
"""

from google.oauth2 import id_token
from google.auth.transport import requests as g_req
from flask import Flask, request, render_template, make_response, session
from flask import Blueprint, redirect, url_for, current_app
from models.users import GoogleUser
from models.engine.db_storage import DBStorage
from models import storage_type
import pyotp
import uuid
import logging

CLIENT_ID = ('518132922807-8vsde0i71v5nktavtssmt1j8vtugvu6o'
             '.apps.googleusercontent.com')


def google_signin(req):
    """Parse request and render sign in for google users
    @param (req): <Request().request obj>
    Return: render_template() redirect()
    """
    if req.form.get('credential'):
        try:
            token = req.form.get('credential')
            idinfo = id_token.verify_oauth2_token(token,
                                                  g_req.Request(),
                                                  CLIENT_ID)
            if idinfo:
                email = idinfo.get('email')
                google_id = idinfo.get("sub")
        except ValueError:
            return render_template('signin.html',
                                   info="Invalid account!",
                                   cache_id=uuid.uuid4())
        # check for existence of user via google id
        g_user = storage_type.fetch_user(None, None, google_id)
        if not g_user:
            return render_template('signin.html', info="Oops.. No user Found",
                                   cache_id=uuid.uuid4())

        # fetch user info since user exists via google id
        session['logged_in'] = True
        session['email'] = email
        session['user_id'] = g_user.id
        session.permanet = True
        return redirect(url_for("web_app.dashboard", user_id=g_user.id))
