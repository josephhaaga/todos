import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)

def list_todos():
    """List all todos in the database."""
    for num in range(5):
        click.echo(f'todo #{num}')
    
    

if __name__ == '__main__':
    list_todos()
