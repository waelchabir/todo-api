from uuid import uuid4

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