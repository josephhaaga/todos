# Application Factory
# Set up DB
# Set up Service with connection to DB
# Construct CLI and add functions
# Return application instance

from service import TodoService
from db import Database

import click
from pathlib import Path
from os import path


# Create or open instance folder, and pass to Database 
home = str(Path.home())
# Ensure .todos folder exists
app_instance_directory = path.join(home, '.todos')
Path(app_instance_directory).mkdir(parents=True, exist_ok=True)

path_to_db_file = path.join(app_instance_directory, 'db.json') 
print(f"Starting app with JSON in {path_to_db_file}")
todo_service = TodoService(Database(path_to_db_file))

@click.group()
def cli():
    pass

@click.command()
@click.option("--all", "status", flag_value="ALL")
@click.option("--not-started", "status", flag_value="NOT_STARTED")
@click.option("--in-progress", "status", flag_value="IN_PROGRESS")
@click.option("--completed", "status", flag_value="COMPLETED")
def show(status, tag=None):
    todos = todo_service.list(status, tag)
    breakpoint()
    for todo in todos:
        print(todo)

@click.command()
@click.argument("description")
@click.option("-t", "--tags")
def add(description, tags=[]):
    """Add a todo item to the database."""
    doc_id = todo_service.create(description, tags) 
    click.echo(f"Inserted TODO #{doc_id}: {description}")


cli.add_command(show)
cli.add_command(add)

if __name__ == "__main__":
    cli()
