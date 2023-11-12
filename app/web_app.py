#!/usr/bin/pytohn3
"""Web app using flask"""


from flask import Flask, request, render_template, make_response
from models.ezy import Ezy
from models.engine.db_storage import DBStorage
from shortner.qr_img_gen import qr_gen
import uuid
import logging


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_input():

    if request.method == "POST":
        user_input = request.form.get("user_input")
        user_output = request.form.get("user_output")

        wor = "Long link enterd is not a valid address"
        alias_error = "Alias has been used please try another"

        ezy_instance = Ezy()
        ezy_instance.original_url = user_input

        if user_output:
            ezy_instance.short_url = user_output

            alias = func_alias(ezy_instance, user_output)
            if alias == "alias exist original url valid":
                """This would check if the alias exists before saving
                and if the original url entered by user is valid"""
                # ezy_instance.remove_url()  # deletes the created instance
                ezy_instance.save()
                return homepage('', 404, '', alias_error, '')

            ezy_instance.save()
            if alias == "alias exist original url invalid":
                ezy_instance.remove_url()  # deletes the created instance
                return homepage('', 404, '', '', wor)
            if alias == "alias doesn't exist original url invalid":
                ezy_instance.remove_url()  # deletes the created instance
                return homepage('', 404, '', '', wor)
            if alias == "alias doesn't exist original url valid":
                short_url = ezy_instance.url()
                qr_file_path = qr_gen(short_url)
                return homepage(short_url, 200, qr_file_path, '', '')
        else:
            ezy_instance.exists()  # check for existence before saving
            ezy_instance.save()
            if ezy_instance.url():
                short_url = ezy_instance.url()
                qr_file_path = qr_gen(short_url)
                return homepage(short_url, 200, qr_file_path, '', '')
            else:
                return homepage('', 404, '', '', wor)

    return render_template('homepage.html', cache_id=uuid.uuid4())


def homepage(short_url, status_code, qr_file_path, alias, word):
    """Renders homepage"""
    return render_template('homepage.html', url=short_url,
                           status=status_code, qr_image=qr_file_path,
                           alias_status=alias, word=word)


def func_alias(ezy_instance, user_output):
    """Handles:
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


@app.route('/about')
def about():
    """Renders static page"""
    return render_template('staticpage.html', cache_id=uuid.uuid4())


"""Perfroms redirection
HOW IT WORKS:
A user accesses a short URL like ezyurl.com/shortlink in their web browser
Nginx Receives the Request
Nginx Routes the Request to Python Script
Nginx is configured to route all incoming requests to a specific location
Nginx sends the request to this Python script for processing.
The URL path, /shortlink is passed as part of the request to the Python script
The script looks up the original URL associated with shortlink from database
If it finds a matching original URL, it creates a redirection response.
it generates an HTTP redirection response using a 302 status code.
Nginx receives the HTTP redirection response from the Python script.
Nginx processes the redirection response and performs the redirection
based on the Location header. It tells the user's web browser to navigate
to the original URL.
"""


@app.route('/<shortlink>')
def redirect(shortlink):
    """Perfroms redirection
    """
    result = DBStorage()
    url = result.redirect(shortlink)

    if url is not None:
        if not url.startswith("https://") and not url.startswith("http://"):
            url = 'http://' + url

        response = make_response('')
        response.headers['Location'] = url
        response.status_code = 302
        return response
    else:
        return render_template('not_found.html', cache_id=uuid.uuid4(),
                               code=404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
