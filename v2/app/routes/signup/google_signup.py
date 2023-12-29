#!/usr/bin/python3
"""Renders google signup
"""

from google.oauth2 import id_token
from google.auth.transport import requests as g_req
from flask import Flask, request, render_template, make_response, session
from flask import Blueprint, redirect, url_for, current_app
from models.users import GoogleUser
from models.engine.db_storage import DBStorage
import pyotp
import uuid
import logging

CLIENT_ID = ('518132922807-8vsde0i71v5nktavtssmt1j8vtugvu6o'
             '.apps.googleusercontent.com')


def google_signup(req):
    """Parse request and handles google users signup
    @param (req): <Request.request object>
    Return: redirect(), render_template()
    """
    if req.form.get('credential'):
        try:
            token = req.form.get('credential')
            idinfo = id_token.verify_oauth2_token(token,
                                                  g_req.Request(),
                                                  CLIENT_ID)
            if idinfo:
                email = idinfo.get('email')
                first_name = idinfo.get('given_name')
                last_name = idinfo.get('family_name')
                verified = idinfo.get('email_verified')
                google_id = idinfo.get("sub")
                profile_pic = idinfo.get("picture")
                two_factor = pyotp.random_base32()
        except ValueError:
            return render_template('signup.html',
                                   info="Invalid account!",
                                   cache_id=uuid.uuid4())
        new_user = GoogleUser()

        # checks if google id already exist in database
        if new_user.exists(None, None, google_id):
            return render_template('signup.html',
                                   info="user already exits!",
                                   cache_id=uuid.uuid4())

        new_user.email = email
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.two_factor = two_factor
        new_user.verified = verified
        new_user.google_id = google_id
        new_user.profile_pic = profile_pic

        new_user.save()
        session['user_email'] = email
        session['logged_in'] = True
        session['user_id'] = new_user.id
        session.permanent = True
        return redirect(url_for("web_app.dashboard", user_id=new_user.id))
