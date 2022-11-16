import os
from uuid import uuid4

from chalice import Chalice

app = Chalice(app_name=os.getenv('APPLICATION_NAME'))
app.debug = True
_DB = None


class InMemoryTodoDB(object):
    def __init__(self, state=None):
        if state is None:
            state = {}
        self._state = state

    def list_all_items(self):
        all_items = []
        for v in self.list_items_values():
            all_items.append(v)
        return all_items

    def list_items_values(self):
        return self._state.values()

    def add_item(self, title, description=''):
        uid = str(uuid4())
        self._state[uid] = {
            'id': uid,
            'title': title,
            'description': description
        }
        return uid

    def get_item(self, uid):
        return self._state[uid]

    def delete_item(self, uid):
        del self._state[uid]

    def update_item(self, uid, title=None, description=None):
        item = self._state[uid]
        if title is not None:
            item['title'] = title
        if description is not None:
            item['description'] = description


def get_app_db():
    global _DB
    if _DB is None:
        _DB = InMemoryTodoDB()
    return _DB


@app.route('/'+os.getenv('API_VERSION')+'/todo', methods=['GET'])
def list_todos():
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
        title=body.get('title'),
        description=body.get('description')
        )

@app.route('/'+os.getenv('API_VERSION')+'/todo/{uid}', methods=['DELETE'])
def delete_todo(uid):
    return get_app_db().delete_item(uid)