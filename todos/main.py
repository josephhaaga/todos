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
@click.option("--all", "status", flag_value="ALL", default=True)
@click.option("--not-started", "status", flag_value="NOT_STARTED")
@click.option("--in-progress", "status", flag_value="IN_PROGRESS")
@click.option("--completed", "status", flag_value="COMPLETED")
@click.option("-t", "--tag", "tag", default=False)
def list(status, tag=False):
    """List all todos in the database."""
    click.echo(f"Searching for todos with status: {status} and tag: {tag}")
    contains_tag = lambda tags: (tag in tags) if tag else True
    # contains_tag = lambda tags: len(tags) > 0
    status_matches = (
        lambda todo_status: True
        if status == "ALL"
        else todo_status == Status[status].value
    )

    Todo = Query()
    todos = db.search(
        (Todo.status.test(status_matches)) & (Todo.tags.test(contains_tag))
    )
    for todo in todos:
        click.echo(f"#{todo.doc_id}: {format_pretty_todo(todo)}")

def format_pretty_todo(todo):
    return (
        f'{todo["description"]}'
        f'\t{" ".join(todo["tags"])}'
    )

@click.command()
@click.argument("description")
@click.option("-t", "--tags")
def add(description, tags=[]):
    """Add a todo item to the database."""
    todo = {
        "description": description,
        "inserted_at": dt.utcnow().isoformat(),
        "status": Status.NOT_STARTED.value,
        "tags": tags.split(",") if tags else [],
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
