#!/usr/bin/python3
"""Creates an endpoint to retrive all records of a url
"""


from api.ezy_v1.views import app_views
from flasgger.utils import swag_from
from flask import abort, jsonify, request
from models import storage_type
from models.ezy import Ezy


@app_views.route('/status')
def get_status():
    """Test function for api"""
    return {"Status": "OK"}


@app_views.route('/long', methods=['GET'])
def get_records_from_long_link():
    """This function return all records/objects of
    the long link
    """
    long_link = request.args.get('url')
    all_records = storage_type.all(long_link)
    if not all_records:
        abort(404)

    return jsonify(all_records)


@app_views.route('/short/<short_link>', methods=['GET'])
def get_record_based_on_short_url(short_link):
    """returns a record of the short link
    """
    record = storage_type.all(None, short_link)
    if not record:
        abort(404)

    return jsonify(record)
