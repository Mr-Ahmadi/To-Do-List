"""
Task model for the ToDoList application.

This module defines the Task class which represents a task entity
within a project.
"""

from datetime import datetime
from typing import Optional


class Task:
    """
    Represents a task in the ToDoList system.

    A task belongs to a project and contains details about a specific
    work item including title, description, deadline, and status.

    Attributes:
        id (int): Unique identifier for the task
        title (str): Title of the task
        description (str): Detailed description of the task
        project_id (int): ID of the project this task belongs to
        deadline (Optional[datetime]): Optional deadline for the task
        status (str): Current status of the task (todo/in_progress/done)
        created_at (datetime): Timestamp when the task was created
        updated_at (datetime): Timestamp when the task was last updated
    """

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        project_id: int,
        deadline: Optional[datetime] = None,
        status: str = "todo",
    ):
        """
        Initialize a new Task instance.

        Args:
            id (int): Unique identifier for the task
            title (str): Title of the task
            description (str): Detailed description of the task
            project_id (int): ID of the project this task belongs to
            deadline (Optional[datetime]): Optional deadline for the task
            status (str): Initial status of the task (default: 'todo')
        """
        self.id = id
        self.title = title
        self.description = description
        self.project_id = project_id
        self.deadline = deadline
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(
        self,
        title: str = None,
        description: str = None,
        deadline: Optional[datetime] = None,
        status: str = None,
    ) -> None:
        """
        Update task details.

        Args:
            title (str, optional): New title for the task
            description (str, optional): New description for the task
            deadline (Optional[datetime], optional): New deadline for the task
            status (str, optional): New status for the task
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if deadline is not None:
            self.deadline = deadline
        if status is not None:
            self.status = status
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """
        Return string representation of the task.

        Returns:
            str: Formatted string with task details
        """
        deadline_str = (
            self.deadline.strftime("%Y-%m-%d") if self.deadline else "No deadline"
        )
        return (
            f"Task ID: {self.id}\n"
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Status: {self.status}\n"
            f"Deadline: {deadline_str}\n"
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def __repr__(self) -> str:
        """
        Return developer-friendly representation of the task.

        Returns:
            str: String representation for debugging
        """
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"status='{self.status}', project_id={self.project_id})"
        )
