"""
Project model for the ToDoList application.

This module defines the Project class which represents a project entity
containing multiple tasks.
"""

from datetime import datetime
from typing import List


class Project:
    """
    Represents a project in the ToDoList system.

    A project is a container for multiple tasks and has its own metadata
    including name, description, and timestamps.

    Attributes:
        id (int): Unique identifier for the project
        name (str): Name of the project
        description (str): Detailed description of the project
        created_at (datetime): Timestamp when the project was created
        updated_at (datetime): Timestamp when the project was last updated
        tasks (List[Task]): List of tasks belonging to this project
    """

    def __init__(self, id: int, name: str, description: str):
        """
        Initialize a new Project instance.

        Args:
            id (int): Unique identifier for the project
            name (str): Name of the project
            description (str): Detailed description of the project
        """
        self.id = id
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks: List = []

    def update(self, name: str = None, description: str = None) -> None:
        """
        Update project details.

        Args:
            name (str, optional): New name for the project
            description (str, optional): New description for the project
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()

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
            f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Number of Tasks: {len(self.tasks)}"
        )

    def __repr__(self) -> str:
        """
        Return developer-friendly representation of the project.

        Returns:
            str: String representation for debugging
        """
        return f"Project(id={self.id}, name='{self.name}', tasks={len(self.tasks)})"
