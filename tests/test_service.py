import os

import pytest

from todos.service import TodoService
from todos.db import Database


class TestTodoService:
    @pytest.fixture(scope="module")
    def db_backed_service(self):
        # TODO This should be only in db.py. Service.py tests should rely on a stubbed DB
        test_db_file = "./test_db.json"
        db = Database(test_db_file)
        serv = TodoService(db)
        yield serv
        os.remove(test_db_file)  # Teardown

    def test_create(self, db_backed_service):
        task_id = db_backed_service.create("Some task")
        assert task_id == 1

    def test_note(self, db_backed_service):
        db_backed_service.note(1, "This is an example note")
        assert db_backed_service.get(1).notes[0]["content"] == "This is an example note"

    def test_get(self, db_backed_service):
        task = db_backed_service.get(1)
        assert task.task_id == 1

    def test_list(self, db_backed_service):
        tasks = db_backed_service.list()
        assert (len(tasks)) == 1

    def test_estimate_time(self, db_backed_service):
        db_backed_service.estimate_time(1, 4.0)
        # How can we alter this test so we don't rely on .get()?
        task = db_backed_service.get(1)
        assert task.estimate_in_hours == 4.0

    def test_start(self, db_backed_service):
        db_backed_service.start(1)
        task = db_backed_service.get(1)
        assert "started_at" in task.__dict__

    def test_complete(self, db_backed_service):
        db_backed_service.complete(1)
        task = db_backed_service.get(1)
        assert "completed_at" in task.__dict__

    def test_delete(self, db_backed_service):
        db_backed_service.delete(1)
        assert len(db_backed_service.list()) == 0  # smelly
