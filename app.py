import os
from uuid import uuid4

from chalice import Chalice

app = Chalice(app_name=os.getenv('APPLICATION_NAME'))
app.debug = True
_DB = None
DEFAULT_USERNAME = 'default'


class InMemoryTodoDB(object):
    def __init__(self, state=None):
        if state is None:
            state = {}
        self._state = state

    def list_all_items(self):
        all_items = []
        for username in self._state:
            all_items.extend(self.list_items(username))
        return all_items

    def list_items(self, username=DEFAULT_USERNAME):
        return self._state.get(username, {}).values()

    def add_item(self, title, description='', username=DEFAULT_USERNAME):
        if username not in self._state:
            self._state[username] = {}
        uid = str(uuid4())
        self._state[username][uid] = {
            'id': uid,
            'title': title,
            'description': description
        }
        return uid

    def get_item(self, uid, username=DEFAULT_USERNAME):
        return self._state[username][uid]

    def delete_item(self, uid, username=DEFAULT_USERNAME):
        del self._state[username][uid]

    def update_item(self, uid, description=None, state=None,
                    metadata=None, username=DEFAULT_USERNAME):
        item = self._state[username][uid]
        if description is not None:
            item['description'] = description
        if state is not None:
            item['state'] = state
        if metadata is not None:
            item['metadata'] = metadata


def get_app_db():
    global _DB
    if _DB is None:
        _DB = InMemoryTodoDB()
    return _DB


@app.route('/'+os.getenv('API_VERSION')+'/todo', methods=['GET'])
def list_todos():
    print('Listing todos ...')
    return get_app_db().list_all_items()

@app.route('/'+os.getenv('API_VERSION')+'/todo', methods=['PUT'])
def create_todo():
    body = app.current_request.json_body
    return get_app_db().add_item(
        title=body.get('title'),
        description=body.get('description'),
    )

@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['GET'])
def get_todo(uid):
    return get_app_db().get_item(uid)

@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['PUT'])
def update_todo(uid):
    body = app.current_request.json_body
    get_app_db().update_item(
        uid,
        description=body.get('description'),
        state=body.get('state'),
        metadata=body.get('metadata'))

@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['DELETE'])
def delete_todo(uid):
    return get_app_db().delete_item(uid)