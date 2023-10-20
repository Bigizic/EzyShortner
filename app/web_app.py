#!/usr/bin/pytohn3
"""Web app using flask"""


from flask import Flask, request, render_template
from models.ezy import Ezy
from models.engine.db_storage import DBStorage
from shortner.qr_img_gen import qr_gen


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_input():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        ezy_instance = Ezy(original_url=user_input)
        ezy_instance.exists()  # check for existence before saving
        ezy_instance.save()
        word = "Long link enterd is not a valid address"
        short_url = ezy_instance.url() if ezy_instance.url() else word
        status_code = 200 if short_url != word else 404

        qr_file_path = qr_gen(short_url) if short_url != word else ''

        return render_template('homepage.html', url=short_url,
                               status=status_code, qr_image=qr_file_path)

    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
