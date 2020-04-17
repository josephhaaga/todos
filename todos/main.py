import click
from tinydb import TinyDB, Query
from datetime import datetime as dt

db = TinyDB('db.json')

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
    todo = {'description': description, 'inserted_at': dt.utcnow().isoformat()}
    db.insert(todo)
    click.echo(f'Inserted {todo}')


cli.add_command(add)
cli.add_command(list)


if __name__ == '__main__':
    cli() 
