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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
