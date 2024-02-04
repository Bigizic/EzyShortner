#!/usr/bin/python3
"""Renders ezy signup
"""

import bcrypt
import datetime
from flask import Flask, request, render_template, make_response, session
from flask import Blueprint, redirect, url_for, current_app
from models.account_information import AccountInformation as ACCI
from models.users import EzyUser
from models.engine.db_storage import DBStorage
import pyotp
import uuid
import logging

TIME = '%Y-%m-%d %H:%M:%S'


def ezy_signup(req):
    """Parse request and handles ezy users signup
    @param (req): <Request.request object>
    Return: redirect(), render_template()
    """
    if req.form.get("email"):
        email = req.form.get("email")
        # protect against attacks
        if len(email) > 128 or not email.find('@') or email is None:
            return render_template('signup.html',
                                   info="email is invalid!",
                                   cache_id=uuid.uuid4())
        password = req.form.get("pass")
        if len(password) > 128 or password is None:
            ps = "Oops.. check the password"
            return render_template('signup.html', info=ps,
                                   cache_id=uuid.uuid4())

        first_name = req.form.get("first_name")
        last_name = req.form.get("last_name")

        if len(first_name) >= 127 or len(last_name) >= 127:
            return render_template('signup.html',
                                   info="names too long",
                                   cache_id=uuid.uuid4())
        new_user = EzyUser()

        # checks if ezy user exits by email
        if new_user.exists(None, email):
            return render_template('signup.html', info="email already exits!",
                                   cache_id=uuid.uuid4())

        new_user.email = email
        new_user.password = password
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.two_factor = pyotp.random_base32()
        new_user.profile_pic = email[0].upper() + email[1].upper()
        # new_user.verified = "YES" if code == otps else "NO"

        new_user.save()
        session['user_email'] = email
        session['logged_in'] = True
        session['user_id'] = new_user.id
        session.permanent = True

        u_a = ACCI()
        u_a.user_id = new_user.id
        u_a.login_time = datetime.datetime.utcnow().strftime(TIME)
        u_a.save()

        return redirect(url_for("web_app.dashboard", user_id=new_user.id))
