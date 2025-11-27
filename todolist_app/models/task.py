"""
Task model for the ToDoList application with SQLAlchemy ORM support.

This module defines the Task entity for database storage using SQLAlchemy ORM.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from todolist_app.db import Base


class TaskStatus(enum.Enum):
    """
    Enumeration of possible task statuses.
    
    Attributes:
        TODO: Task is pending and not yet started
        IN_PROGRESS: Task is currently being worked on
        DONE: Task has been completed
        OVERDUE: Task has passed its deadline without completion
    """
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    OVERDUE = "overdue"


class Task(Base):
    """
    Represents a task in the ToDoList system (ORM Entity).

    A task belongs to a project and contains details about a specific
    work item including title, description, deadline, and status.
    This class uses SQLAlchemy ORM for database persistence.

    Attributes:
        id (int): Unique identifier for the task (auto-generated)
        title (str): Title of the task
        description (str): Detailed description of the task
        status (TaskStatus): Current status of the task
        deadline (Optional[datetime]): Optional deadline for the task
        created_at (datetime): Timestamp when the task was created
        updated_at (datetime): Timestamp when the task was last updated
        closed_at (Optional[datetime]): Timestamp when the task was marked as done
        project_id (int): Foreign key referencing the parent project
        project (Project): Relationship to parent project
    """
    
    __tablename__ = "tasks"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Task details
    title = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    deadline = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    closed_at = Column(DateTime, nullable=True)
    
    # Foreign key to Project
    project_id = Column(
        Integer, 
        ForeignKey('projects.id', ondelete='CASCADE'), 
        nullable=False
    )
    
    # Relationship with Project
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self) -> str:
        """
        Return developer-friendly representation of the task.

        Returns:
            str: String representation for debugging
        """
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"status='{self.status.value}', project_id={self.project_id})"
        )
    
    def __str__(self) -> str:
        """
        Return string representation of the task.

        Returns:
            str: Formatted string with task details
        """
        deadline_str = (
            self.deadline.strftime("%Y-%m-%d") if self.deadline else "No deadline"
        )
        closed_str = (
            self.closed_at.strftime("%Y-%m-%d %H:%M:%S") 
            if self.closed_at else "Not completed"
        )
        
        return (
            f"Task ID: {self.id}\n"
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Status: {self.status.value}\n"
            f"Deadline: {deadline_str}\n"
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Closed: {closed_str}"
        )
    
    def to_dict(self) -> dict:
        """
        Convert task to dictionary representation.
        
        Returns:
            dict: Dictionary containing all task attributes
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'project_id': self.project_id
        }
