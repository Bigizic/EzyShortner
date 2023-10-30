#!/usr/bin/pytohn3
"""Web app using flask"""


from flask import Flask, request, render_template
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

        ezy_instance = Ezy()
        ezy_instance.original_url = user_input
        if user_output:
            ezy_instance.short_url = user_output

        alias = (ezy_instance.exists(user_output) if user_output else
                 ezy_instance.exists())
        # app.logger.warning(alias)

        # ezy_instance.exists()  # check for existence before saving
        ezy_instance.save()
        wor = "Long link enterd is not a valid address"

        short_url = (ezy_instance.url() if ezy_instance.url()
                     and not alias else '')

        word = wor if not short_url and not alias else ''
        status_code = 200 if len(short_url) > 1 and not alias else 404

        qr_file_path = qr_gen(short_url) if len(
                    short_url) > 1 and not alias else ''
        if not alias:
            alias = ''

        return render_template('homepage.html', url=short_url,
                               status=status_code, qr_image=qr_file_path,
                               alias_status=alias, word=word)

    return render_template('homepage.html', cache_id=uuid.uuid4())

@app.route('/about')
def about():
    return render_template('aboutuspage.html', cache_id=uuid.uuid4())


"""Perfroms redirection
HOW IT WORKS:
A user accesses a short URL like ezyurl.com/shortlink in their web browser
Nginx Receives the Request
Nginx Routes the Request to Python Script
Nginx is configured to route all incoming requests to a specific location
Nginx sends the request to this Python script for processing.
The URL path, /shortlink is passed as part of the request to the Python script
The script looks up the original URL associated with shortlink from MYSQL database
If it finds a matching original URL, it proceeds to create a redirection response.
it generates an HTTP redirection response using a 302 status code.
Nginx receives the HTTP redirection response from the Python script.
Nginx processes the redirection response and performs the redirection based on the
Location header. It tells the user's web browser to navigate to the original URL.
"""


@app.route('/move/<shortlink>')
def redirect(shortlink):
    """Perfroms redirection
    """
    short = shortlink.split('/')[3]
    result = DBStorage()
    dict_result = result.all(None, short)
    app.logger(dict_result)
    return



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
