import click
from datetime import datetime
from todolist_app.db.session import get_db_context
from todolist_app.services.task_service import TaskService


@click.command("tasks:autoclose-overdue")
def autoclose_overdue():
    """
    Auto-close all overdue tasks:
    deadline < now AND status != done
    """
    with get_db_context() as db:
        service = TaskService(db)
        count = service.autoclose_overdue_tasks()

    click.echo(f"✔ {count} overdue tasks were automatically closed.")
