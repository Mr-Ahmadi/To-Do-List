"""
Task Service for business logic.

This module handles business logic for task operations,
including validation and coordination between repositories.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from todolist_app.repositories.task_repository import TaskRepository
from todolist_app.models.task import Task, TaskStatus
from todolist_app.exceptions.custom_exceptions import (
    ValidationException,
    MaxLimitException,
)
from todolist_app.utils.validators import Validator
from todolist_app.utils.config import Config


class TaskService:
    """
    Service class for task business logic.
    
    This class implements business rules, validation, and coordinates
    between the repository layer and presentation layer.
    Uses Dependency Injection pattern to receive repository instance.
    """

    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db (Session): SQLAlchemy database session
        """
        self.repository = TaskRepository(db)

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: Optional[str] = None,
        status: str = "todo"
    ) -> Task:
        """
        Create a new task with validation.

        Args:
            project_id (int): ID of parent project
            title (str): Task title
            description (str): Task description
            deadline (Optional[str]): Deadline in YYYY-MM-DD format
            status (str): Initial status (default: 'todo')

        Returns:
            Task: Created task

        Raises:
            MaxLimitException: If task limit exceeded
            ValidationException: If validation fails
        """
        # Check maximum limit
        if self.repository.count_by_project(project_id) >= Config.get_max_tasks():
            raise MaxLimitException(
                f"Cannot create more than {Config.get_max_tasks()} tasks per project."
            )

        # Validate inputs
        Validator.validate_task_title(title)
        Validator.validate_task_description(description)
        Validator.validate_status(status)
        
        # Parse and validate deadline
        deadline_dt = Validator.validate_deadline(deadline)
        
        # Convert string status to TaskStatus enum
        task_status = TaskStatus(status)

        # Create task through repository
        return self.repository.create(
            title=title,
            description=description,
            project_id=project_id,
            deadline=deadline_dt,
            status=task_status
        )

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Get task by ID.

        Args:
            task_id (int): Task ID

        Returns:
            Task: Found task

        Raises:
            TaskNotFoundException: If task not found
        """
        return self.repository.get_by_id(task_id)

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """
        Get all tasks for a specific project.

        Args:
            project_id (int): Project ID

        Returns:
            List[Task]: List of tasks
        """
        return self.repository.get_by_project(project_id)

    def get_tasks_by_status(
        self, 
        project_id: int, 
        status: str
    ) -> List[Task]:
        """
        Get tasks by status with validation.

        Args:
            project_id (int): Project ID
            status (str): Status to filter by

        Returns:
            List[Task]: List of tasks with specified status

        Raises:
            ValidationException: If status is invalid
        """
        Validator.validate_status(status)
        task_status = TaskStatus(status)
        return self.repository.get_by_status(project_id, task_status)

    def get_overdue_tasks(
        self, 
        project_id: Optional[int] = None
    ) -> List[Task]:
        """
        Get overdue tasks.

        Args:
            project_id (Optional[int]): Filter by project (if provided)

        Returns:
            List[Task]: List of overdue tasks
        """
        return self.repository.get_overdue_tasks(project_id)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[str] = None,
        status: Optional[str] = None
    ) -> Task:
        """
        Update task with validation.

        Args:
            task_id (int): ID of task to update
            title (Optional[str]): New title
            description (Optional[str]): New description
            deadline (Optional[str]): New deadline in YYYY-MM-DD format
            status (Optional[str]): New status

        Returns:
            Task: Updated task

        Raises:
            TaskNotFoundException: If task not found
            ValidationException: If validation fails
        """
        # Validate inputs if provided
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

        # Convert status to enum if provided
        task_status = TaskStatus(status) if status else None

        # Update through repository
        return self.repository.update(
            task_id=task_id,
            title=title,
            description=description,
            deadline=deadline_dt,
            status=task_status
        )

    def delete_task(self, task_id: int) -> bool:
        """
        Delete task.

        Args:
            task_id (int): ID of task to delete

        Returns:
            bool: True if deleted successfully

        Raises:
            TaskNotFoundException: If task not found
        """
        return self.repository.delete(task_id)

    def mark_task_as_done(self, task_id: int) -> Task:
        """
        Mark task as done.

        Args:
            task_id (int): ID of task

        Returns:
            Task: Updated task

        Raises:
            TaskNotFoundException: If task not found
        """
        return self.repository.mark_as_done(task_id)

    def mark_tasks_as_overdue(self, project_id: Optional[int] = None) -> int:
        """
        Mark overdue tasks as overdue status.

        Args:
            project_id (Optional[int]): Filter by project (if provided)

        Returns:
            int: Number of tasks marked as overdue
        """
        overdue_tasks = self.get_overdue_tasks(project_id)
        count = 0
        
        for task in overdue_tasks:
            self.repository.mark_as_overdue(task.id)
            count += 1
        
        return count

    def search_tasks(self, project_id: int, query: str) -> List[Task]:
        """
        Search tasks by title or description.

        Args:
            project_id (int): Project ID
            query (str): Search term

        Returns:
            List[Task]: List of matching tasks
        """
        return self.repository.search(project_id, query)

    def get_task_count(self, project_id: int) -> int:
        """
        Get task count for a project.

        Args:
            project_id (int): Project ID

        Returns:
            int: Number of tasks
        """
        return self.repository.count_by_project(project_id)

    def autoclose_overdue_tasks(self):
        return self.repository.autoclose_overdue_tasks()