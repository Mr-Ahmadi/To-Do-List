import click
from todolist_app.commands.autoclose_overdue import autoclose_overdue


@click.group()
def cli():
    """Command-line tools for scheduled or manual operations."""
    pass


# Register commands
cli.add_command(autoclose_overdue)
