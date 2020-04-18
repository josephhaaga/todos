from enum import Enum
import click
from tinydb import TinyDB, Query
from datetime import datetime as dt

db = TinyDB('db.json')

Status = Enum('Status', 'NOT_STARTED IN_PROGRESS COMPLETED')
# TODO: determine a way to track when status changes occur! Perhaps a [] of change events?
# TODO: utility script to walk thru a source code directory and add these TODO comments to the database! And supplement them with info about where they were found!

@click.group()
def cli():
    pass

@click.command()
def list():
    """List all todos in the database."""
    todos = db.all()
    for todo in todos: 
        click.echo(todo)
    
@click.command()
@click.argument('description')
def add(description):
    """Add a todo item to the database."""
    todo = {'description': description, 'inserted_at': dt.utcnow().isoformat(), 'status': Status.NOT_STARTED.value}
    doc_id = db.insert(todo)
    click.echo(f'Inserted TODO #{doc_id}: {todo}')

@click.command()
@click.argument('todo_id')
def complete(todo_id):
    """Mark a todo item as completed."""


cli.add_command(add)
cli.add_command(list)


if __name__ == '__main__':
    cli() 
