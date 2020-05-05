from datetime import datetime as dt
import pytz
from enum import Enum
from todos.models import Todo, TodoSchema, Tag, TagSchema

Status = Enum("Status", "NOT_STARTED IN_PROGRESS COMPLETED")


class TodoService:
    storage = None

    def __init__(self, storage):
        self.storage = storage

    def list(self, status: str = None, tag: str = None):
        """List Todos."""
        if not status and not tag:
            todos = self.storage.list()
            return [TodoSchema().load(item) for item in todos]
        args = {'status': Status[status].value, 'tag': tag}
        conditions = {k: v for k, v in args.items() if v is not None}
        todos = self.storage.find(conditions)
        return [TodoSchema().load(item) for item in todos]

    def create(self, title=None, tags=[]):
        """Create a Todo."""
        todo = Todo(title)
        todo_id = self.storage.create(TodoSchema().dump(todo))
        print(f"Created Todo #{todo_id}")
        return todo_id

    def delete(self, todo_id):
        """Delete a Todo."""
        self.storage.delete(todo_id)
        print(f"Removed Todo #{todo_id}")
        return todo_id

    def start(self, todo_id):
        """Start working on a Todo."""
        todo = TodoSchema().load(self.storage.get(todo_id))
        todo.start()
        self.storage.update(todo_id, TodoSchema().dump(todo))
        return todo

    def complete(self, todo_id):
        """Finish working on a Todo."""
        todo = TodoSchema().load(self.storage.get(todo_id))
        todo.complete()
        self.storage.update(todo_id, TodoSchema().dump(todo))
        return todo
