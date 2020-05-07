from datetime import datetime as dt
from enum import Enum
from typing import List
from os import getcwd

import pytz

from todos.models import Todo, TodoSchema, Tag, TagSchema, load_todo, dump_todo


class TodoService:
    storage = None

    def __init__(self, storage):
        self.storage = storage

    def create(self, title=None, tags=[]) -> int:
        current_directory = getcwd()
        task = Todo(title=title, inserted_at=dt.now(), location=current_directory)
        task_id = self.storage.create(dump_todo(task))
        return task_id

    def note(self, task_id: int, note: str):
        todo = load_todo(self.storage.get(task_id))
        todo.add_note(note)
        self.storage.update(task_id, dump_todo(todo))
        return task_id

    def get(self, task_id: int):
        task = self.storage.get(task_id)
        return load_todo(task)

    def list(self, status: str = None, tag: str = None) -> List:
        if not status and not tag:
            status = "NOT_STARTED"
        args = {"status": status, "tag": tag}
        conditions = {k: v for k, v in args.items() if v is not None}
        todos = self.storage.find(conditions)
        return [load_todo(item) for item in todos]

    def estimate_time(self, todo_id: int, estimate_in_hours: float):
        todo = load_todo(self.storage.get(todo_id))
        todo.set_estimate(estimate_in_hours)
        self.storage.update(todo_id, dump_todo(todo))
        return todo

    def start(self, todo_id) -> Todo:
        todo = load_todo(self.storage.get(todo_id))
        todo.start()
        self.storage.update(todo_id, dump_todo(todo))
        return todo

    def complete(self, todo_id) -> Todo:
        todo = load_todo(self.storage.get(todo_id))
        todo.complete()
        self.storage.update(todo_id, dump_todo(todo))
        return todo

    def delete(self, todo_id) -> int:
        self.storage.delete(todo_id)
        return todo_id
