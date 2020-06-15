"""Application factory."""
from pathlib import Path
from os import path

from todos.services.TodoService import TodoService
from todos.services.AgendaService import AgendaService
from todos.db import Database
from todos.utils import create_cli


def create_app():
    """Creates and returns an instance of the application."""
    app_instance_directory = path.join(Path.home(), ".todos")
    Path(app_instance_directory).mkdir(parents=True, exist_ok=True)

    path_to_db_file = path.join(app_instance_directory, "db.json")

    app = type("App", (), {})
    app.db = Database(path_to_db_file)
    app.todo_service = TodoService(app.db)
    app.agenda_service = AgendaService(app)
    return app


def main():
    App = create_app()
    create_cli(App)


if __name__ == "__main__":
    main()
