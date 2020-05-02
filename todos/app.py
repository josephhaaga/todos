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

def create_app():
    # Create or open instance folder, and pass to Database 
    home = str(Path.home())
    app_instance_directory = path.join(home, '.todos')
    Path(app_instance_directory).mkdir(parents=True, exist_ok=True)

    path_to_db_file = path.join(app_instance_directory, 'db.json') 
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
        for todo in todos:
            click.echo(todo)

    @click.command()
    @click.argument("description")
    @click.option("-t", "--tags")
    def add(description, tags=[]):
        """Add a todo item to the database."""
        doc_id = todo_service.create(description, tags) 
        click.echo(f"Inserted TODO #{doc_id}: {description}")

    @click.command()
    @click.argument("todo_id", type=int)
    def start(todo_id):
        """Start working on a todo item."""
        started_todo = todo_service.start(todo_id)
        click.echo(f"Started {started_todo}")

    @click.command()
    @click.argument("todo_id", type=int)
    def complete(todo_id):
        """Finish working on a todo item."""
        finished_todo = todo_service.complete(todo_id)
        click.echo(f"Finished {finished_todo}")

    @click.command()
    @click.argument("todo_id", type=int)
    def delete(todo_id):
        """Delete a todo item."""
        result = todo_service.delete(todo_id)
        if result:
            click.echo(f"Successfully deleted.")
        else:
            click.echo(f"Error occurred while deleting {todo_id}")

    cli.add_command(show)
    cli.add_command(add)
    cli.add_command(start)
    cli.add_command(complete)
    cli.add_command(delete)

    return cli()

if __name__ == "__main__":
    create_app()
