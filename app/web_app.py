#!/usr/bin/pytohn3
"""Web app using flask"""


from flask import Flask, request, render_template
from shortner.models.ezy import create_ezy_instance
from shortner.models.engine.db_storage import DBStorage

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_input():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        ezy_instance = create_ezy_instance(user_input)
        ezy_instance.save()

    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
