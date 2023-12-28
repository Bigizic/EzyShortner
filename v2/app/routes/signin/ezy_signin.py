#!/usr/bin/python3
"""Renders Google users sign in
"""

import bcrypt
from flask import Flask, request, render_template, make_response, session
from flask import Blueprint, redirect, url_for, current_app
from models import storage_type as st
from models.users import EzyUser
from models.engine.db_storage import DBStorage
import pyotp
import uuid
import logging


def ezy_signin(req):
    """Renders a normal user sign in
    @param (req): <Request().request obj>
    Return: render_template() redirect
    """
    if req.form.get('email'):
        email = req.form.get("email")
        # protect against attacks
        if len(email) > 128 or not email.find('@') or email is None:
            return render_template('signin.html',
                                   info="email is invalid!",
                                   cache_id=uuid.uuid4())
        password = req.form.get("pass")
        if len(password) > 128 or password is None:
            ps = "Oops.. check the password"
            return render_template('signin.html', info=ps,
                                   cache_id=uuid.uuid4())

        # check if user exists by email
        e_user = EzyUser().exists(None, email)
        if not e_user:
            return render_template('signin.html', info="Oops.. No user Found",
                                   cache_id=uuid.uuid4())
        # fetch user by email to retrieve password and user id
        user_info = st.fetch_user(None, email)

        if user_info:
            user_pass = user_info.password
            passs = bcrypt.checkpw(password.encode(), user_pass.encode())

            if passs:
                session['logged_in'] = True
                session['email'] = email
                session['user_id'] = user_info.id
                session.permanent = True
                return redirect(url_for("web_app.dashboard",
                                user_id=user_info.id))
            else:
                return render_template('signin.html',
                                       info="Oops wrong information",
                                       cache_id=uuid.uuid4())
