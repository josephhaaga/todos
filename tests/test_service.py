import pytest
from todos.service import TodoService

class MockDB:
    @staticmethod
    def create(item_description, item_tags=[]):
        return 1

    @staticmethod
    def delete(item_id):
        return 1

class TestTodoService:
    service = TodoService(MockDB())
    
    def test_create(self):
        assert self.service.create(description="Some todo") == 1
    
    def test_delete(self):
        assert self.service.delete(1) == 1
    
