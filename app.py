import os

from chalice import Chalice, Response
from helpers.response import get_success_response, get_error_response
from helpers.db import InMemoryTodoDB

app = Chalice(app_name=os.getenv('APPLICATION_NAME'))
app.debug = True
_DB = None


def get_app_db():
    global _DB
    if _DB is None:
        _DB = InMemoryTodoDB()
    return _DB

@app.route('/'+os.getenv('API_VERSION')+'/todo', methods=['GET'])
def list_todos():
    try:
        return get_app_db().list_all_items()
    except:
        return get_error_response('TODO_LISTING_ERROR_MESSAGE')

@app.route('/'+os.getenv('API_VERSION')+'/todo', methods=['PUT'])
def create_todo():
    body = app.current_request.json_body
    try:
        get_app_db().add_item(
            title=body.get('title'),
            description=body.get('description'),
        )
        return get_success_response('TODO_CREATION_SUCCESS_MESSAGE')
    except:
        return get_error_response('TODO_CREATION_ERROR_MESSAGE')

@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['GET'])
def get_todo(uid):
    try:
        return [get_app_db().get_item(uid)]
    except:
        return get_error_response('TODO_GETONE_ERROR_MESSAGE')

@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['PUT'])
def update_todo(uid):
    body = app.current_request.json_body
    try:
        get_app_db().update_item(
            uid,
            title=body.get('title'),
            description=body.get('description')
            )
        return get_success_response('TODO_UPDATE_SUCCESS_MESSAGE')
    except:
        return get_error_response('TODO_UPDATE_ERROR_MESSAGE')


@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['DELETE'])
def delete_todo(uid):
    try:
        get_app_db().delete_item(uid)
        return get_success_response('TODO_DELETE_SUCCESS_MESSAGE')
    except:
        return get_error_response('TODO_DELETE_ERROR_MESSAGE')