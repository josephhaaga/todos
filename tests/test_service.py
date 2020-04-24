import pytest
from todos.service import TodoService

class MockDB:
    items = [] 
    def create(self, item_description, item_tags=[]):
        self.items += [{'description': item_description, 'tags': item_tags}]
        print(f"self.items: {str(self.items)}")
        return len(self.items)

    def delete(self, item_id):
        del self.items[item_id - 1]
        return item_id

class TestTodoService:
    service = TodoService(MockDB())
    
    def test_create(self):
        assert self.service.create(description="Some todo") == 1
    
    def test_delete(self):
        assert self.service.delete(1) == 1
    
