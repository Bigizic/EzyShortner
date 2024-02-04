#!/usr/bin/python3
"""A function that check in the database if alias exists or not
@param (ezy_instance): <instance> of Ezy() class
@param (user_ouput): <str> from request.method.get

Return: if alias exist or not
"""
from models.ezy import Ezy


def func_alias(ezy_instance: Ezy, user_output: str) -> str:
    """
    @param (ezy_instance): <Ezy> an instance of Ezy Module from app route
    @param (user_output): <str> Basically user entered alias from html form

    Handles:
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
