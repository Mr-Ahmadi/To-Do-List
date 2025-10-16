"""
Task Manager module for the ToDoList application.

This module provides the TaskManager class which handles all
business logic related to task operations within a project.
"""

from datetime import datetime
from typing import List, Optional

from todolist_app.exceptions.custom_exceptions import (
    MaxLimitException,
    TaskNotFoundException,
)
from todolist_app.models.project import Project
from todolist_app.models.task import Task
from todolist_app.utils.config import Config
from todolist_app.utils.validators import Validator


class TaskManager:
    """
    Manager class for handling task operations within a project.

    This class provides CRUD operations for tasks and enforces
    business rules such as maximum task limits per project.

    Attributes:
        project (Project): The project this manager is associated with
        next_id (int): Counter for generating unique task IDs
    """

    def __init__(self, project: Project):
        """
        Initialize TaskManager for a specific project.

        Args:
            project (Project): The project to manage tasks for
        """
        self.project = project
        self.next_id: int = 1

    def create_task(
        self,
        title: str,
        description: str,
        deadline: Optional[str] = None,
        status: str = "todo",
    ) -> Task:
        """
        Create a new task in the project.

        Args:
            title (str): Title of the task
            description (str): Description of the task
            deadline (Optional[str]): Deadline in YYYY-MM-DD format
            status (str): Initial status (default: 'todo')

        Returns:
            Task: The newly created task

        Raises:
            MaxLimitException: If maximum number of tasks is reached
            ValidationException: If validation fails
            InvalidStatusException: If status is invalid
            InvalidDateException: If deadline is invalid
        """
        # Check maximum limit
        if len(self.project.tasks) >= Config.get_max_tasks():
            raise MaxLimitException(
                f"Cannot create more than {Config.get_max_tasks()} tasks per project."
            )

        # Validate inputs
        Validator.validate_task_title(title)
        Validator.validate_task_description(description)
        Validator.validate_status(status)

        # Validate and parse deadline
        deadline_dt = Validator.validate_deadline(deadline)

        # Create task
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            project_id=self.project.id,
            deadline=deadline_dt,
            status=status,
        )

        self.project.tasks.append(task)
        self.next_id += 1

        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the project.

        Returns:
            List[Task]: List of all tasks
        """
        return self.project.tasks

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Get a task by its ID.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Task: The requested task

        Raises:
            TaskNotFoundException: If task with given ID is not found
        """
        for task in self.project.tasks:
            if task.id == task_id:
                return task

        raise TaskNotFoundException(
            f"Task with ID {task_id} not found in project '{self.project.name}'."
        )

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Get all tasks with a specific status.

        Args:
            status (str): Status to filter by

        Returns:
            List[Task]: List of tasks with the specified status

        Raises:
            InvalidStatusException: If status is invalid
        """
        Validator.validate_status(status)
        return [task for task in self.project.tasks if task.status == status]

    def update_task(
        self,
        task_id: int,
        title: str = None,
        description: str = None,
        deadline: Optional[str] = None,
        status: str = None,
    ) -> Task:
        """
        Update an existing task.

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task
            deadline (Optional[str], optional): New deadline in YYYY-MM-DD format
            status (str, optional): New status for the task

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundException: If task is not found
            ValidationException: If validation fails
            InvalidStatusException: If status is invalid
            InvalidDateException: If deadline is invalid
        """
        task = self.get_task_by_id(task_id)

        # Validate new values if provided
        if title is not None:
            Validator.validate_task_title(title)

        if description is not None:
            Validator.validate_task_description(description)

        if status is not None:
            Validator.validate_status(status)

        # Parse deadline if provided
        deadline_dt = None
        if deadline is not None:
            deadline_dt = Validator.validate_deadline(deadline)

        # Update task
        task.update(
            title=title, description=description, deadline=deadline_dt, status=status
        )

        return task

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task from the project.

        Args:
            task_id (int): ID of the task to delete

        Raises:
            TaskNotFoundException: If task is not found
        """
        task = self.get_task_by_id(task_id)
        self.project.tasks.remove(task)

    def mark_task_as_done(self, task_id: int) -> Task:
        """
        Mark a task as done.

        Args:
            task_id (int): ID of the task to mark as done

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundException: If task is not found
        """
        task = self.get_task_by_id(task_id)
        task.update(status="done")
        return task

    def get_task_count(self) -> int:
        """
        Get the total number of tasks in the project.

        Returns:
            int: Number of tasks
        """
        return len(self.project.tasks)

    def get_pending_tasks(self) -> List[Task]:
        """
        Get all tasks that are not done.

        Returns:
            List[Task]: List of pending tasks (todo or in_progress)
        """
        return [task for task in self.project.tasks if task.status != "done"]

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all tasks that are overdue.

        Returns:
            List[Task]: List of overdue tasks
        """
        today = datetime.now().date()
        return [
            task
            for task in self.project.tasks
            if task.deadline
            and task.deadline.date() < today
            and task.status != "done"
        ]

    def search_tasks(self, search_term: str) -> List[Task]:
        """
        Search tasks by title or description.

        Args:
            search_term (str): Term to search for

        Returns:
            List[Task]: List of matching tasks
        """
        search_lower = search_term.lower()
        return [
            task
            for task in self.project.tasks
            if search_lower in task.title.lower()
            or search_lower in task.description.lower()
        ]
