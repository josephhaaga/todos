# Application Factory
# Set up DB
# Set up Service with connection to DB
# Construct CLI and add functions
# Return application instance

from todos.service import TodoService
from todos.db import Database
from todos.utils import create_cli

from pathlib import Path
from os import path

def create_app():
    # Create or open instance folder, and pass to Database 
    home = str(Path.home())
    app_instance_directory = path.join(home, '.todos')
    Path(app_instance_directory).mkdir(parents=True, exist_ok=True)

    path_to_db_file = path.join(app_instance_directory, 'db.json') 

    app = type("App", (), {})
    app.todo_service = TodoService(Database(path_to_db_file))
    return app

if __name__ == "__main__":
    app = create_app()
    create_cli(app)
