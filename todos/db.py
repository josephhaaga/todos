from tinydb import TinyDB, Query, where
from functools import reduce


class Database:
    db = None

    def __init__(self, path_to_database_file="db.json"):
        self.db = TinyDB(path_to_database_file)

    def create(self, item: dict):
        """Insert an item into the database."""
        document_id = self.db.insert(item)
        return document_id

    def list(self):
        """Return all items in the database."""
        return self.db.all()

    def find(self, clauses: dict):
        """Search the database for items matching a set of criteria."""
        if len(clauses) == 0:
            return self.list()
        # TODO: support operators other than ==
        terms = [where(key) == val for key, val in clauses.items()]
        built_query = reduce(lambda a, b: a & b, terms)
        return self.db.search(built_query)

    def get(self, document_id: int):
        """Retrieve an item from the database."""
        # document_id = int(document_id)
        return self.db.get(doc_id=document_id)

    def update(self, document_id: int, updates_to_make: dict):
        """Update an item in the database."""
        # document_id = int(document_id)
        updated_doc_ids = self.db.update(updates_to_make, doc_ids=[document_id])
        return updated_doc_ids[0]

    def delete(self, document_id: int):
        """Remove an item from the database."""
        # document_id = int(document_id)
        return self.db.remove(doc_ids=[document_id])
