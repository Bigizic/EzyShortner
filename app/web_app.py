#!/usr/bin/pytohn3
"""Web app using flask"""


from flask import Flask, request, render_template
from models.ezy import Ezy
from models.engine.db_storage import DBStorage

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_input():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        ezy_instance = Ezy(user_input)
        ezy_instance.exists()  # check for existence before saving
        ezy_instance.save()
        return render_template('homepage.html', url=ezy_instance.url())

    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
