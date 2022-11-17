import os

import boto3
from chalice import Chalice
from helpers.response import get_success_response, get_error_response
import helpers.db as db


app = Chalice(app_name=os.getenv('APPLICATION_NAME'))
db.init_api_table_dynamodb()
app.debug = False
_DB = db.get_todo_db()


@app.route('/'+os.getenv('API_VERSION')+'/todo', methods=['GET'])
def list_todos():
    try:
        return _DB.list_all_items()
    except Exception as e:
        return get_error_response('TODO_LISTING_ERROR_MESSAGE')

@app.route('/'+os.getenv('API_VERSION')+'/todo', methods=['PUT'])
def create_todo():
    body = app.current_request.json_body
    try:
        _DB.add_item(
            title=body.get('title'),
            description=body.get('description'),
        )
        return get_success_response('TODO_CREATION_SUCCESS_MESSAGE')
    except:
        return get_error_response('TODO_CREATION_ERROR_MESSAGE')

@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['GET'])
def get_todo(uid):
    try:
        return [_DB.get_item(uid)]
    except:
        return get_error_response('TODO_GETONE_ERROR_MESSAGE')

@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['PUT'])
def update_todo(uid):
    body = app.current_request.json_body
    try:
        _DB.update_item(
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
        _DB.delete_item(uid)
        return get_success_response('TODO_DELETE_SUCCESS_MESSAGE')
    except:
        return get_error_response('TODO_DELETE_ERROR_MESSAGE')