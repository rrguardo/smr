# -*- coding: utf-8 -*-
"""
    flaskapp.app_exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~

    App custom exceptions.

"""

from flask import jsonify
from flaskapp import app

class InvalidUsage(Exception):
    """ Custom exception example."""
    status_code = 400
    
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
            self.payload = payload
    
    def to_dict(self):
        """ ret the dictionary"""
        rvd = dict(self.payload or ())
        rvd['message'] = self.message
        return rvd

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """ Error handle example."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
                           
