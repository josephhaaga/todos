from enum import Enum
import click
from tinydb import TinyDB, Query
from datetime import datetime as dt

db = TinyDB("db.json")

Status = Enum("Status", "NOT_STARTED IN_PROGRESS COMPLETED")


@click.group()
def cli():
    pass

@click.command()
def list():
    """List all todos in the database."""
    todos = db.all()
    for todo in todos:
        click.echo(f"#{todo.doc_id}: {todo}")

@click.command()
@click.argument("description")
def add(description):
    """Add a todo item to the database."""
    todo = {
        "description": description,
        "inserted_at": dt.utcnow().isoformat(),
        "status": Status.NOT_STARTED.value,
    }
    doc_id = db.insert(todo)
    click.echo(f"Inserted TODO #{doc_id}: {todo}")

@click.command()
@click.argument("todo_id", type=int)
def start(todo_id):
    """Mark a todo item as started."""
    todo = db.get(doc_id=todo_id)
    if "started_at" in todo:
        click.echo(f'TODO #{todo_id} was already started at {todo["started_at"]}')
        return False
    todo = db.update(
        {"status": Status.IN_PROGRESS.value, "started_at": dt.utcnow().isoformat()},
        doc_ids=[todo_id],
    )
    click.echo(f"Started TODO #{todo_id}: {db.get(doc_id=todo_id)}")

@click.command()
@click.argument("todo_id", type=int)
def complete(todo_id):
    """Mark a todo item as completed."""
    todo = db.get(doc_id=todo_id)
    if "completed_at" in todo:
        click.echo(f'TODO #{todo_id} was already completed at {todo["completed_at"]}')
        return False
    todo = db.update(
        {"status": Status.COMPLETED.value, "completed_at": dt.utcnow().isoformat()},
        doc_ids=[todo_id],
    )
    click.echo(f"Completed TODO #{todo_id}: {db.get(doc_id=todo_id)}")


cli.add_command(add)
cli.add_command(list)
cli.add_command(start)
cli.add_command(complete)

if __name__ == "__main__":
    cli()
