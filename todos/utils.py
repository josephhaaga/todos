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
    def now():
        todos = app.todo_service.list("IN_PROGRESS", None)
        for todo in todos:
            click.echo(todo)

    @click.command()
    @click.argument("title")
    @click.option("-t", "--tags")
    def add(title, tags=[]):
        """Add a task to the database."""
        doc_id = app.todo_service.create(title, tags)
        click.echo(f"Inserted TODO #{doc_id}: {title}")

    @click.command()
    def then():
        """Suggests tasks to work on next."""
        not_started_todos = app.todo_service.list("NOT_STARTED")
        for task in not_started_todos:
            response = True if input(f"Start {task}? (Y/N) ") == "Y" else False
            if response:
                # start(task.task_id)
                started_todo = app.todo_service.start(task.task_id)
                click.echo(f"Started {started_todo}")
                return
        pass

    @click.command()
    @click.argument("task_id", type=int)
    @click.argument("estimate_in_hours", type=float)
    def estimate(task_id, estimate_in_hours):
        """Set the time estimate for a task."""
        updated_task = app.todo_service.estimate_time(task_id, estimate_in_hours)
        click.echo(
            f"#{task_id} is now estimate to take {updated_task.estimate_in_hours} hours."
        )

    @click.command()
    @click.argument("todo_id", type=int)
    def start(todo_id):
        """Start working on task."""
        started_todo = app.todo_service.start(todo_id)
        click.echo(f"Started {started_todo}")

    @click.command()
    @click.argument("todo_id", type=int)
    def complete(todo_id):
        """Finish working on a task."""
        finished_todo = app.todo_service.complete(todo_id)
        click.echo(f"Finished {finished_todo}")

    @click.command()
    @click.argument("todo_id", type=int)
    def delete(todo_id):
        """Delete a task."""
        result = app.todo_service.delete(todo_id)
        if result:
            click.echo(f"Successfully deleted.")
        else:
            click.echo(f"Error occurred while deleting {todo_id}")

    cli.add_command(now)
    cli.add_command(add)
    cli.add_command(show)
    cli.add_command(estimate)
    cli.add_command(then)
    cli.add_command(start)
    cli.add_command(complete)
    cli.add_command(delete)

    return cli()
