from tinydb import TinyDB, Query


class Database:
    db = TinyDB("db.json")

    def create(item: dict):
        """Insert an item into the database."""
        document_id = db.insert(item)
        return document_id

    def find():
        """Search the database for items matching a set of criteria."""
        return db.search()

    def get(document_id: int):
        """Retrieve an item from the database."""
        return db.get(doc_id=document_id)

    def update(document_id: int, updates_to_make: dict):
        """Update an item in the database."""
        return db.update(updates_to_make, doc_ids=[document_id])

    def delete(document_id: int):
        """Remove an item from the database."""
        return db.remove(doc_ids=[document_id])
