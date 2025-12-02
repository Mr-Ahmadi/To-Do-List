"""
Project model for the ToDoList application with SQLAlchemy ORM support.

This module defines the Project entity for database storage using SQLAlchemy ORM.
"""

from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from todolist_app.db import Base


class Project(Base):
    """
    Represents a project in the ToDoList system (ORM Entity).

    A project is a container for multiple tasks and has its own metadata
    including name, description, and timestamps.
    This class uses SQLAlchemy ORM for database persistence.

    Attributes:
        id (int): Unique identifier for the project (auto-generated)
        name (str): Name of the project (unique)
        description (str): Detailed description of the project
        created_at (datetime): Timestamp when the project was created
        tasks (List[Task]): List of tasks belonging to this project
    """
    
    __tablename__ = "projects"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Project details
    name = Column(String(500), nullable=False, unique=True)
    description = Column(String(2000), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship with Tasks (one-to-many)
    # cascade="all, delete-orphan" means when project is deleted, all tasks are deleted too
    tasks = relationship(
        "Task", 
        back_populates="project", 
        cascade="all, delete-orphan",
        lazy="selectin"  # Automatically load tasks when querying project
    )
    
    def __repr__(self) -> str:
        """
        Return developer-friendly representation of the project.

        Returns:
            str: String representation for debugging
        """
        return f"Project(id={self.id}, name='{self.name}', tasks={len(self.tasks)})"
    
    def __str__(self) -> str:
        """
        Return string representation of the project.

        Returns:
            str: Formatted string with project details
        """
        return (
            f"Project ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Number of Tasks: {len(self.tasks)}"
        )
    
    def to_dict(self) -> dict:
        """
        Convert project to dictionary representation.
        
        Returns:
            dict: Dictionary containing all project attributes and tasks
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'tasks': [task.to_dict() for task in self.tasks]
        }
