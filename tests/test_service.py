import pytest
from todos.service import TodoService

class MockDB:
    items = [] 
    
    def __init__(self, items=[]):
        self.items = items

    def create(self, item_description, item_tags=[]):
        self.items += [{'description': item_description, 'tags': item_tags}]
        return len(self.items)

    def update(self, item_id, changes):
        item = self.items[item_id - 1]
        self.items[item_id - 1] = {**item, **changes}
        print(f"self.items: {str(self.items)}")
        return item_id

    def delete(self, item_id):
        del self.items[item_id - 1]
        return item_id

class TestTodoService:
    
    def test_create(self):
        service = TodoService(MockDB())
        assert service.create(description="Some todo") == 1
    
    def test_delete(self):
        service = TodoService(MockDB([{'description': 'task'}]))
        assert service.delete(1) == 1

    def test_start(self):
        service = TodoService(MockDB([{'description': 'some task'}]))
        service.start(1)
        assert 'started_at' in service.storage.items[0]

    def test_complete(self):
        service = TodoService(MockDB([{'description': 'some task'}]))
        service.complete(1)
        assert 'completed_at' in service.storage.items[0]