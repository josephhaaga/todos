"""Random utility functions related to the Todo app."""
import datetime

import click


def pretty_print_date(datestamp: datetime.datetime):
    """Returns a nicely-formatted datestring."""
    return datestamp.strftime("%h %d, %Y %l:%M %p")


def add_seed_data(service):
    """Add a few fake tasks to the Todo list."""
    service.create("Add an ncurses tui to tasks-app")
    service.create("Review marshmallow and plan how it can be used")
    service.create("Read some Real Python")
    service.create("Work on tasks")
    service.create("Do the Kedro spaceflights tutorial")
    service.create("Draft up a finance-app with fake data")
    service.create("install mint on thinkpad")


def create_cli(app):
    """Generate the CLI commands."""

    @click.group()
    def cli():
        pass

    @click.command()
    @click.option("--all", "status", flag_value="ALL")
    @click.option("--not-started", "status", flag_value="NOT_STARTED")
    @click.option("--in-progress", "status", flag_value="IN_PROGRESS")
    @click.option("--completed", "status", flag_value="COMPLETED")
    def show(status, tag=None):
        """List all tasks."""
        tasks = app.todo_service.list(status, tag)
        for task in tasks:
            click.echo(task)

    @click.command()
    @click.argument("task_id", type=int)
    def get(task_id):
        """Show details about a task."""
        task = app.todo_service.get(task_id)
        click.echo(task.get_details())

    @click.command()
    def now():
        """List tasks currently IN_PROGRESS."""
        tasks = app.todo_service.list("IN_PROGRESS", None)
        for task in tasks:
            click.echo(task)

    @click.command()
    @click.argument("title")
    @click.option("-t", "--tags")
    def add(title, tags=None):
        """Add a task."""
        doc_id = app.todo_service.create(title)
        click.echo(f"Inserted task #{doc_id}: {title}")

    @click.command()
    @click.argument("task_id", type=int)
    @click.argument("note", type=str)
    def note(task_id, note):
        """Add a note to a task."""
        app.todo_service.note(task_id, note)
        click.echo(f"Added note to task #{task_id}")

    @click.command()
    def then():
        """Suggests tasks to work on next."""
        not_started_tasks = app.todo_service.list("NOT_STARTED")
        for task in not_started_tasks:
            user_response = input(f"Start {task}? (Y/N) ").upper()
            response = user_response == "Y"
            if response:
                started_task = app.todo_service.start(task.task_id)
                click.echo(f"Started {started_task}")
                return

    @click.command()
    @click.argument("task_id", type=int)
    @click.argument("estimate_in_hours", type=float)
    def estimate(task_id, estimate_in_hours):
        """Set the time estimate for a task."""
        app.todo_service.estimate_time(task_id, estimate_in_hours)
        click.echo(f"#{task_id} estimate set to {estimate_in_hours} hours.")

    @click.command()
    @click.argument("task_id", type=int)
    def start(task_id):
        """Start working on task."""
        app.todo_service.start(task_id)
        click.echo(f"Started {task_id}")

    @click.command()
    @click.argument("task_id", type=int)
    def complete(task_id):
        """Finish working on a task."""
        app.todo_service.complete(task_id)
        click.echo(f"Finished {task_id}")

    @click.command()
    @click.argument("task_id", type=int)
    def delete(task_id):
        """Delete a task."""
        app.todo_service.delete(task_id)
        click.echo(f"Successfully deleted.")

    @click.command()
    def agenda():
        app.agenda_service.run()

    cli.add_command(show)
    cli.add_command(get)
    cli.add_command(now)
    cli.add_command(add)
    cli.add_command(note)
    cli.add_command(then)
    cli.add_command(estimate)
    cli.add_command(start)
    cli.add_command(complete)
    cli.add_command(delete)
    cli.add_command(agenda)

    return cli()
