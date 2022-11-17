import os

from chalice import Response

def get_success_response(msg_key=None):
    message = '{"message": "%s"}'%(os.getenv(msg_key))
    return Response(body=message,
            headers={'Content-Type': 'application/json'},
            status_code=200)

def get_error_response(msg_key=None):
    message = '{"error": "%s"}'%(os.getenv(msg_key))
    return Response(body=message,
            headers={'Content-Type': 'application/json'},
            status_code=400)