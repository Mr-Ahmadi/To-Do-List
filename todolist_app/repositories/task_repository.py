"""
Task Repository for database operations.

This module handles all database queries related to Task entities.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from todolist_app.models.task import Task, TaskStatus
from todolist_app.exceptions.repository_exceptions import (
    TaskNotFoundException,
    DatabaseOperationException,
)


class TaskRepository:
    """
    Repository class for Task database operations.
    
    This class follows the Repository pattern and handles all
    database interactions for Task entities using SQLAlchemy ORM.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with database session.

        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db

    def create(
        self,
        title: str,
        description: str,
        project_id: int,
        deadline: Optional[datetime] = None,
        status: TaskStatus = TaskStatus.TODO
    ) -> Task:
        """
        Create a new task in database.

        Args:
            title (str): Task title
            description (str): Task description
            project_id (int): ID of parent project
            deadline (Optional[datetime]): Task deadline
            status (TaskStatus): Initial status

        Returns:
            Task: Created task with generated ID

        Raises:
            DatabaseOperationException: If creation fails
        """
        try:
            task = Task(
                title=title,
                description=description,
                project_id=project_id,
                deadline=deadline,
                status=status
            )
            
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            
            return task
            
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationException(
                f"Failed to create task: {str(e)}"
            )

    def get_by_id(self, task_id: int) -> Task:
        """
        Get task by ID.

        Args:
            task_id (int): Task ID to search for

        Returns:
            Task: Found task

        Raises:
            TaskNotFoundException: If task not found
        """
        task = self.db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise TaskNotFoundException(
                f"Task with ID {task_id} not found."
            )
        
        return task

    def get_by_project(self, project_id: int) -> List[Task]:
        """
        Get all tasks for a specific project.

        Args:
            project_id (int): Project ID

        Returns:
            List[Task]: List of tasks in the project
        """
        return self.db.query(Task).filter(
            Task.project_id == project_id
        ).order_by(Task.created_at.desc()).all()

    def get_by_status(
        self, 
        project_id: int, 
        status: TaskStatus
    ) -> List[Task]:
        """
        Get all tasks with specific status in a project.

        Args:
            project_id (int): Project ID
            status (TaskStatus): Status to filter by

        Returns:
            List[Task]: List of tasks with specified status
        """
        return self.db.query(Task).filter(
            Task.project_id == project_id,
            Task.status == status
        ).order_by(Task.created_at.desc()).all()

    def get_overdue_tasks(self, project_id: Optional[int] = None) -> List[Task]:
        """
        Get all overdue tasks (deadline passed and not done).

        Args:
            project_id (Optional[int]): Filter by project ID (if provided)

        Returns:
            List[Task]: List of overdue tasks
        """
        query = self.db.query(Task).filter(
            Task.deadline < datetime.utcnow(),
            Task.status != TaskStatus.DONE,
            Task.status != TaskStatus.OVERDUE
        )
        
        if project_id is not None:
            query = query.filter(Task.project_id == project_id)
        
        return query.all()

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[datetime] = None,
        status: Optional[TaskStatus] = None
    ) -> Task:
        """
        Update task information.

        Args:
            task_id (int): ID of task to update
            title (Optional[str]): New title
            description (Optional[str]): New description
            deadline (Optional[datetime]): New deadline
            status (Optional[TaskStatus]): New status

        Returns:
            Task: Updated task

        Raises:
            TaskNotFoundException: If task not found
            DatabaseOperationException: If update fails
        """
        try:
            task = self.get_by_id(task_id)

            if title is not None:
                task.title = title
            
            if description is not None:
                task.description = description
            
            if deadline is not None:
                task.deadline = deadline
            
            if status is not None:
                task.status = status
                
                # Set closed_at when task is marked as done
                if status == TaskStatus.DONE and task.closed_at is None:
                    task.closed_at = datetime.utcnow()
                # Clear closed_at if task is reopened
                elif status != TaskStatus.DONE:
                    task.closed_at = None

            self.db.commit()
            self.db.refresh(task)
            
            return task
            
        except TaskNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationException(
                f"Failed to update task: {str(e)}"
            )

    def delete(self, task_id: int) -> bool:
        """
        Delete task from database.

        Args:
            task_id (int): ID of task to delete

        Returns:
            bool: True if deleted successfully

        Raises:
            TaskNotFoundException: If task not found
            DatabaseOperationException: If deletion fails
        """
        try:
            task = self.get_by_id(task_id)
            
            self.db.delete(task)
            self.db.commit()
            
            return True
            
        except TaskNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationException(
                f"Failed to delete task: {str(e)}"
            )

    def mark_as_done(self, task_id: int) -> Task:
        """
        Mark task as done and set closed_at timestamp.

        Args:
            task_id (int): ID of task to mark as done

        Returns:
            Task: Updated task

        Raises:
            TaskNotFoundException: If task not found
        """
        return self.update(task_id, status=TaskStatus.DONE)

    def mark_as_overdue(self, task_id: int) -> Task:
        """
        Mark task as overdue.

        Args:
            task_id (int): ID of task to mark as overdue

        Returns:
            Task: Updated task

        Raises:
            TaskNotFoundException: If task not found
        """
        return self.update(task_id, status=TaskStatus.OVERDUE)

    def search(self, project_id: int, query: str) -> List[Task]:
        """
        Search tasks by title or description within a project.

        Args:
            project_id (int): Project ID to search within
            query (str): Search term

        Returns:
            List[Task]: List of matching tasks
        """
        search_pattern = f"%{query}%"
        return self.db.query(Task).filter(
            Task.project_id == project_id,
            (Task.title.ilike(search_pattern)) |
            (Task.description.ilike(search_pattern))
        ).order_by(Task.created_at.desc()).all()

    def count_by_project(self, project_id: int) -> int:
        """
        Count tasks in a specific project.

        Args:
            project_id (int): Project ID

        Returns:
            int: Number of tasks
        """
        return self.db.query(Task).filter(
            Task.project_id == project_id
        ).count()
