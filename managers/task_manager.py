from typing import List, Optional
from datetime import datetime
from models.project import Project
from models.task import Task
from utils.config import Config
from utils.validators import Validator
from exceptions import (
    TaskNotFoundException,
    MaxLimitException
)


class TaskManager:
    """Manager class for handling task-related operations within a project"""
    
    def __init__(self, project: Project):
        """
        Initialize TaskManager for a specific project.
        
        Args:
            project: The Project instance to manage tasks for
        """
        self.project = project
    
    def create_task(
        self, 
        title: str, 
        description: str, 
        deadline: Optional[str] = None,
        status: str = Config.DEFAULT_STATUS
    ) -> Task:
        """
        Create a new task in the project.
        
        Args:
            title: Task title
            description: Task description
            deadline: Task deadline (format: YYYY-MM-DD, optional)
            status: Task status (default: 'todo')
        
        Returns:
            The created Task instance
        
        Raises:
            ValidationException: If validation fails
            MaxLimitException: If maximum task limit reached
            InvalidStatusException: If status is invalid
            InvalidDateException: If deadline is invalid
        """
        # Validate inputs
        Validator.validate_task_title(title)
        Validator.validate_task_description(description)
        Validator.validate_status(status)
        parsed_deadline = Validator.validate_deadline(deadline)
        
        # Check for maximum limit
        if len(self.project.tasks) >= Config.MAX_NUMBER_OF_TASK:
            raise MaxLimitException(
                f"Maximum number of tasks ({Config.MAX_NUMBER_OF_TASK}) reached "
                f"for project '{self.project.name}'. Cannot create more tasks."
            )
        
        # Create and add the task
        task = Task(
            title=title,
            description=description,
            project_id=self.project.id,
            deadline=parsed_deadline,
            status=status
        )
        self.project.add_task(task)
        return task
    
    def get_task(self, task_id: int) -> Task:
        """
        Get a task by its ID.
        
        Args:
            task_id: ID of the task to retrieve
        
        Returns:
            The Task instance
        
        Raises:
            TaskNotFoundException: If task is not found
        """
        task = self.project.get_task(task_id)
        if task is None:
            raise TaskNotFoundException(
                f"Task with ID {task_id} not found in project '{self.project.name}'."
            )
        return task
    
    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """
        Get all tasks or filter by status.
        
        Args:
            status: Filter by status (optional)
        
        Returns:
            List of Task instances
        
        Raises:
            InvalidStatusException: If status is invalid
        """
        if status:
            Validator.validate_status(status)
        
        return self.project.list_tasks(status=status)
    
    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[str] = None,
        status: Optional[str] = None
    ) -> Task:
        """
        Update a task's details.
        
        Args:
            task_id: ID of the task to update
            title: New task title (optional)
            description: New task description (optional)
            deadline: New task deadline (optional)
            status: New task status (optional)
        
        Returns:
            The updated Task instance
        
        Raises:
            TaskNotFoundException: If task is not found
            ValidationException: If validation fails
            InvalidStatusException: If status is invalid
            InvalidDateException: If deadline is invalid
        """
        task = self.get_task(task_id)
        
        # Validate new values if provided
        if title:
            Validator.validate_task_title(title)
        if description:
            Validator.validate_task_description(description)
        if status:
            Validator.validate_status(status)
        
        parsed_deadline = None
        if deadline:
            parsed_deadline = Validator.validate_deadline(deadline)
        
        # Update the task
        task.update(
            title=title,
            description=description,
            deadline=parsed_deadline,
            status=status
        )
        return task
    
    def change_task_status(self, task_id: int, new_status: str) -> Task:
        """
        Change the status of a task.
        
        Args:
            task_id: ID of the task
            new_status: New status value
        
        Returns:
            The updated Task instance
        
        Raises:
            TaskNotFoundException: If task is not found
            InvalidStatusException: If status is invalid
        """
        task = self.get_task(task_id)
        Validator.validate_status(new_status)
        task.update(status=new_status)
        return task
    
    def delete_task(self, task_id: int) -> None:
        """
        Delete a task from the project.
        
        Args:
            task_id: ID of the task to delete
        
        Raises:
            TaskNotFoundException: If task is not found
        """
        # Verify task exists
        self.get_task(task_id)
        # Remove the task
        self.project.remove_task(task_id)
    
    def __repr__(self) -> str:
        return f"TaskManager(project='{self.project.name}', tasks={len(self.project.tasks)})"
