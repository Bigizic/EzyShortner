#!/usr/bin/python3
""" Flask """


from api.ezy_v1.views import app_views
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from flask import Flask, render_template, make_response, jsonify
from models import storage_type
from werkzeug.exceptions import NotFound


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """close storage type(db)"""
    storage_type.close()


@app.errorhandler(NotFound)
def not_found(error):
    """Handles 404 error

    response:
        404 description: a resource was not found
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
