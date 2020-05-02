from datetime import datetime as dt
import pytz
from enum import Enum
from models import Todo

Status = Enum("Status", "NOT_STARTED IN_PROGRESS COMPLETED")


class TodoService:
    storage = None

    def __init__(self, storage):
        self.storage = storage

    def list(self, status: str = None, tag: str = None):
        """List Todos."""
        todos = None
        if not status and not tag:
            todos = self.storage.list()
            return [Todo(id=item.doc_id, **item) for item in todos]
        args = {'status': Status[status].value, 'tag': tag}
        conditions = {k: v for k, v in args.items() if v is not None}
        todos = self.storage.find(conditions)
        return [Todo(id=item.doc_id, **item) for item in todos]

    def create(self, description=None, tags=[]):
        """Create a Todo."""
        todo = {
            "description": description,
            "inserted_at": dt.utcnow().isoformat(),
            "status": Status.NOT_STARTED.value,
            "tags": tags,
        }
        todo_id = self.storage.create(todo)
        print(f"Created Todo #{todo_id}")
        return todo_id

    def delete(self, todo_id):
        """Delete a Todo."""
        self.storage.delete(todo_id)
        print(f"Removed Todo #{todo_id}")
        return todo_id

    def start(self, todo_id):
        """Start working on a Todo."""
        # This should add a new dict to a list called time_logged
        # e.g. {'start_time': now, }
        now = dt.utcnow().isoformat()
        updated_id = self.storage.update(
            str(todo_id), {"started_at": now, "status": Status.IN_PROGRESS.value}
        )
        return Todo(id=updated_id, **self.storage.get(updated_id))

    def stop(self, todo_id):
        # This should update the 'end_time' of the last dict in the time_logged list.
        """Stop working on a Todo."""

    def delete(self, todo_id):
        """Delete a Todo from the db."""
        self.storage.delete(todo_id)
        return True 

    def complete(self, todo_id):
        """Finish working on a Todo."""
        # call self.stop(todo_id)
        # set completed_at to now
        # update status
        now = dt.utcnow().isoformat()
        updated_id = self.storage.update(
            todo_id, {"completed_at": now, "status": Status.COMPLETED.value}
        )
        return Todo(id=updated_id, **self.storage.get(updated_id))
