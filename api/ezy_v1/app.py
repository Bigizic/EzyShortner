#!/usr/bin/python3
""" EZYURL API configuration using Flask and flasgger """


from api.ezy_v1.views import app_views
from flask_cors import CORS
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger.utils import swag_from
from flask import Flask, render_template, make_response, jsonify
from models import storage_type
from werkzeug.exceptions import NotFound


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # for better readability
app.json_encoder = LazyJSONEncoder
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={r"/api/ezy_v1/*": {"origins": "*"}})

template = dict(swaggerUiPrefix=LazyString(lambda : request.environ.get('HTTP_X_SCRIPT_NAME', '')))


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

app.config['SWAGGER'] = {
    'title': 'Ezy Url Restful API',
    'uiversion': 3
}

Swagger(app, template=template)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
