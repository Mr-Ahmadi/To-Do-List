"""
Scheduler for automatic periodic tasks in the ToDoList application.

This scheduler runs the "autoclose overdue tasks" job every 15 minutes
using the 'schedule' library.

To run:
    poetry run python -m todolist_app.scheduler.scheduler
"""

import time
import schedule
from datetime import datetime

from todolist_app.db.session import get_db_context
from todolist_app.services.task_service import TaskService


def job_autoclose_overdue():
    """
    Close overdue tasks: tasks with deadline < now AND status != 'done'.
    """
    print(f"[{datetime.now()}] Running job: autoclose overdue tasks...")

    with get_db_context() as db:
        service = TaskService(db)
        count = service.autoclose_overdue_tasks()

    print(f"[{datetime.now()}] ✔ {count} overdue tasks were automatically closed.")


def start_scheduler():
    """
    Configure task schedule and start infinite loop.
    """
    print("⏳ Starting scheduler...")

    # Every 15 minutes
    schedule.every(15).seconds.do(job_autoclose_overdue)

    print("✔ Scheduler is running. Press CTRL+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_scheduler()
