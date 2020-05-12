"""Interface and implementation providing database functionality."""
from functools import reduce
from typing import int, List

from tinydb import TinyDB, where
from todos.models import Todo


class Database:
    db = None

    def __init__(self, path_to_database_file="db.json"):
        self.db = TinyDB(path_to_database_file)

    def create(self, item: dict) -> int:
        """Insert an item into the database."""
        document_id = self.db.insert(item)
        return document_id

    def list(self) -> List:
        """Return all items in the database."""
        return self.db.all()

    def find(self, clauses: dict) -> List:
        """Search the database for items matching a set of criteria."""
        if len(clauses) == 0:
            return self.list()
        # TODO: support operators other than ==
        terms = [where(key) == val for key, val in clauses.items()]
        built_query = reduce(lambda a, b: a & b, terms)
        return self.db.search(built_query)

    def get(self, document_id: int) -> Todo:
        """Retrieve an item from the database."""
        return self.db.get(doc_id=document_id)

    def update(self, document_id: int, updates_to_make: dict) -> None:
        """Update an item in the database."""
        self.db.update(updates_to_make, doc_ids=[document_id])

    def delete(self, document_id: int) -> None:
        """Remove an item from the database."""
        self.db.remove(doc_ids=[document_id])
