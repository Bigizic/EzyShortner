#!/usr/bin/python3
"""Function that handles the application interaction

Return: application features
"""

from models.ezy import Ezy
from models.engine.db_storage import DBStorage
from os import environ
from shortner.qr_img_gen import qr_gen
from app.web_app_functions.alias import func_alias
import re
import uuid


def application(user_input: str, user_output: str, user_id: str = None) -> str:
    """
    @param (user_input): <str> accepts user input from request.method.get
        i.e the long link

    @param (user_output): <str> accepts user output from request.method.get
        i.e the alias

    @param (user_id): <str> a uuid.uuid4() id that serves as a user id
    """
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
                     "about", "about_us", "about-us", "dashboard", "ezy.com",
                     "dash_board", "dash-board", "dashboard_", "ezy", "ezy."]

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
