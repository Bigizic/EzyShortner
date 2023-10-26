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
@swag_from('/api/ezy_v1/views/documentation/get_long_link.yml')
def get_records_from_long_link():
    """This function return all records/objects of
    the long link
    0.0.0.0:5001/api/ezy_v1/long?url={long_link}
    """
    long_link = request.args.get('url')
    all_records = storage_type.all(long_link)
    count = storage_type.count(long_link)
    if not all_records:
        abort(404)

    result = {
        'exists': 'ok',
        'number_of_records' if count > 1 else 'number_of_record' : count,
        'data': all_records
    }

    return jsonify(result)


@app_views.route('/short/<short_link>', methods=['GET'])
@swag_from('/api/ezy_v1/views/documentation/get_short_link.yml')
def get_record_based_on_short_url(short_link):
    """returns a record of the short link
    """
    record = storage_type.all(None, short_link)
    count = storage_type.count(None, short_link)
    if not record:
        abort(404)

    result = {
        'exists': 'ok',
        'number_of_record': count,
        'data': record
    }

    return jsonify(result)
    if not record:
        abort(404)

    return jsonify(record)
