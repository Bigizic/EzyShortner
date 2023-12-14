#!/usr/bin/python3
"""Function that renders the homepage
@param (short_url): <str> short_url that user sees when a shortened
link is displayed in browser

@param (status_code): <int> either 200 or 404, if 200 displays the
copy and qr button and other buttons for more functionality

@param (qr_file_path): <str> lets the server know the qr file
path of the qr image

@para (alias): <str> displays alias to user's browser

@param (word): <str> displays long link errors
"""

from flask import render_template
import uuid


def homepage(short_url, status_code, qr_file_path, alias, word):
    """Renders homepage"""
    return render_template('homepage.html', url=short_url,
                           status=status_code, qr_image=qr_file_path,
                           alias_status=alias, word=word,
                           cache_id=uuid.uuid4())
