from datetime import datetime as dt

class TodoService:
    storage = None
    def __init__(self, storage):
        self.storage = storage

    def create(self, description=None, tags=[]):
        """Create a Todo."""
        todo = {
            'description': description,
            'inserted_at': dt.utcnow().isoformat(),
            'tags': tags
        }
        todo_id = self.storage.create(todo)
        print(f"Created Todo #{todo_id}") 
        return todo_id

    def add_tag(self, todo_id):
        """Add a tag to a Todo."""
        pass

    def remove_tag(self, todo_id):
        """Remove a tag from a Todo."""
        pass

    def start(self, todo_id):
        """Start working on a Todo."""
        # This should add a new dict to a list called time_logged
        # e.g. {'start_time': now, }
        pass

    def stop(self, todo_id):
        # This should update the 'end_time' of the last dict in the time_logged list.
        """Stop working on a Todo."""

    def complete(self, todo_id):
        """Finish working on a Todo."""
        pass

    def delete(self, todo_id):
        """Delete a Todo."""
        self.storage.delete(todo_id)
        print(f"Removed Todo #{todo_id}")
        return todo_id
