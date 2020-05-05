from datetime import datetime as dt
from enum import Enum
from typing import List

import pytz

from todos.models import Todo, TodoSchema, Tag, TagSchema, load_todo, dump_todo


class TodoService:
    storage = None

    def __init__(self, storage):
        self.storage = storage

    def create(self, title=None, tags=[]) -> int:
        """Create a task."""
        todo = Todo(title=title, inserted_at=dt.now())
        todo_id = self.storage.create(dump_todo(todo))
        print(f"Created task #{todo_id}")
        return todo_id

    def list(self, status: str = None, tag: str = None) -> List:
        """List tasks."""
        if not status and not tag:
            todos = self.storage.list()
            return [load_todo(item) for item in todos]
        args = {"status": Status[status].value, "tag": tag}
        conditions = {k: v for k, v in args.items() if v is not None}
        todos = self.storage.find(conditions)
        return [load_todo(item) for item in todos]

    def estimate_time(self, todo_id: int, estimate_in_hours: float):
        """Estimate how long a task will take."""
        todo = load_todo(self.storage.get(todo_id))
        todo.set_estimate(estimate_in_hours)
        self.storage.update(todo_id, dump_todo(todo))
        return todo

    def start(self, todo_id) -> Todo:
        """Start working on a task."""
        todo = load_todo(self.storage.get(todo_id))
        todo.start()
        self.storage.update(todo_id, dump_todo(todo))
        return todo

    def complete(self, todo_id) -> Todo:
        """Finish working on a task."""
        todo = load_todo(self.storage.get(todo_id))
        todo.complete()
        self.storage.update(todo_id, dump_todo(todo))
        return todo

    def delete(self, todo_id) -> int:
        """Delete a task."""
        self.storage.delete(todo_id)
        print(f"Removed Todo #{todo_id}")
        return todo_id
