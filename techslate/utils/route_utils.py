import json
from flask import make_response


def get_response(status, body):
    response = make_response(str(body), status)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def error_handler(message, status=400):
    return get_response(status, json.dumps(dict(status="error", message=message)).encode('utf-8'))
