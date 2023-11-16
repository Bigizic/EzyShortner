#!/usr/bin/python3
"""Blueprint for API"""


from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/ezy_v1')

from api.ezy_v1.views.get_records import *
