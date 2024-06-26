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
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # for better readability
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/api/ezy_v1/*": {"origins": "*"}})


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
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
Swagger(app, config=swagger_config)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
