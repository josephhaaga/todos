import click

def add_seed_data(service):
    service.create("Add an ncurses tui to todos-app")
    service.create("Review marshmallow and plan how it can be used")
    service.create("Read some Real Python")
    service.create("Work on todos")
    service.create("Do the Kedro spaceflights tutorial")
    service.create("Draft up a finance-app with fake data")
    service.create("install mint on thinkpad")

def create_cli(app):
    @click.group()
    def cli():
        pass

    @click.command()
    @click.option("--all", "status", flag_value="ALL")
    @click.option("--not-started", "status", flag_value="NOT_STARTED")
    @click.option("--in-progress", "status", flag_value="IN_PROGRESS")
    @click.option("--completed", "status", flag_value="COMPLETED")
    def show(status, tag=None):
        todos = app.todo_service.list(status, tag)
        for todo in todos:
            click.echo(todo)

    @click.command()
    @click.argument("title")
    @click.option("-t", "--tags")
    def add(title, tags=[]):
        """Add a todo item to the database."""
        doc_id = app.todo_service.create(title, tags) 
        click.echo(f"Inserted TODO #{doc_id}: {title}")
    
    @click.command()
    def then():
        """Suggest tasks to a user, starting a todo if they respond Y."""
        not_started_todos = app.todo_service.list("NOT_STARTED")
        for task in not_started_todos:
            response = True if input(f"Start {task}? (Y/N) ") == 'Y' else False
            if response:
                # TODO tech debt
                start(task.id)
                return True
        pass

    @click.command()
    @click.argument("todo_id", type=int)
    def start(todo_id):
        """Start working on a todo item."""
        started_todo = app.todo_service.start(todo_id)
        click.echo(f"Started {started_todo}")

    @click.command()
    @click.argument("todo_id", type=int)
    def complete(todo_id):
        """Finish working on a todo item."""
        finished_todo = app.todo_service.complete(todo_id)
        click.echo(f"Finished {finished_todo}")

    @click.command()
    @click.argument("todo_id", type=int)
    def delete(todo_id):
        """Delete a todo item."""
        result = app.todo_service.delete(todo_id)
        if result:
            click.echo(f"Successfully deleted.")
        else:
            click.echo(f"Error occurred while deleting {todo_id}")

    cli.add_command(show)
    cli.add_command(add)
    cli.add_command(then)
    cli.add_command(start)
    cli.add_command(complete)
    cli.add_command(delete)

    return cli()


