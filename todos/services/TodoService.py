"""Provides functionality on Todo items."""
from datetime import datetime as dt
from typing import List
from os import getcwd

from todos.models import Todo, load_todo, dump_todo


class TodoService:
    """Provides functionality on Todo objects."""

    storage = None

    def __init__(self, storage):
        self.storage = storage

    def create(self, title: str = None) -> int:
        """Create a new Todo item."""
        current_directory = getcwd()
        task = Todo(title=title, inserted_at=dt.now(), location=current_directory)
        task_id = self.storage.create(dump_todo(task))
        return task_id

    def note(self, task_id: int, note: str) -> None:
        """Add a note to a Todo item."""
        todo = load_todo(self.storage.get(task_id))
        todo.add_note(note)
        self.storage.update(task_id, dump_todo(todo))

    def get(self, task_id: int) -> Todo:
        """Get a Todo item."""
        task = self.storage.get(task_id)
        return load_todo(task)

    def list(self, status: str = None, tag: str = None) -> List:
        """Get a list of Todo items."""
        if not status and not tag:
            status = "NOT_STARTED"
        args = {"status": status, "tag": tag}
        conditions = {k: v for k, v in args.items() if v is not None}
        todos = self.storage.find(conditions)
        return [load_todo(item) for item in todos]

    def estimate_time(self, todo_id: int, estimate_in_hours: float) -> None:
        """Set the time estimate for a Todo."""
        todo = load_todo(self.storage.get(todo_id))
        todo.set_estimate(estimate_in_hours)
        self.storage.update(todo_id, dump_todo(todo))

    def start(self, todo_id) -> None:
        """Mark a Todo as started."""
        todo = load_todo(self.storage.get(todo_id))
        todo.start()
        self.storage.update(todo_id, dump_todo(todo))

    def complete(self, todo_id) -> None:
        """Mark a Todo as completed."""
        todo = load_todo(self.storage.get(todo_id))
        todo.complete()
        self.storage.update(todo_id, dump_todo(todo))

    def delete(self, todo_id) -> None:
        """Deletes a Todo."""
        self.storage.delete(todo_id)
