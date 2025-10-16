"""
Project Manager module for the ToDoList application.

This module provides the ProjectManager class which handles all
business logic related to project operations.
"""

from typing import List, Optional

from todolist_app.exceptions.custom_exceptions import (
    DuplicateProjectException,
    MaxLimitException,
    ProjectNotFoundException,
)
from todolist_app.models.project import Project
from todolist_app.utils.config import Config
from todolist_app.utils.validators import Validator


class ProjectManager:
    """
    Manager class for handling project operations.

    This class provides CRUD operations for projects and enforces
    business rules such as maximum project limits and unique names.

    Attributes:
        projects (List[Project]): List of all projects in the system
        next_id (int): Counter for generating unique project IDs
    """

    def __init__(self):
        """Initialize ProjectManager with empty project list."""
        self.projects: List[Project] = []
        self.next_id: int = 1

    def create_project(self, name: str, description: str) -> Project:
        """
        Create a new project.

        Args:
            name (str): Name of the project
            description (str): Description of the project

        Returns:
            Project: The newly created project

        Raises:
            MaxLimitException: If maximum number of projects is reached
            DuplicateProjectException: If a project with the same name exists
            ValidationException: If name or description validation fails
        """
        # Check maximum limit
        if len(self.projects) >= Config.get_max_projects():
            raise MaxLimitException(
                f"Cannot create more than {Config.get_max_projects()} projects."
            )

        # Validate inputs
        Validator.validate_project_name(name)
        Validator.validate_project_description(description)

        # Check for duplicate names
        if self._project_exists_by_name(name):
            raise DuplicateProjectException(
                f"A project with the name '{name}' already exists."
            )

        # Create project
        project = Project(id=self.next_id, name=name, description=description)
        self.projects.append(project)
        self.next_id += 1

        return project

    def get_all_projects(self) -> List[Project]:
        """
        Get all projects.

        Returns:
            List[Project]: List of all projects
        """
        return self.projects

    def get_project_by_id(self, project_id: int) -> Project:
        """
        Get a project by its ID.

        Args:
            project_id (int): ID of the project to retrieve

        Returns:
            Project: The requested project

        Raises:
            ProjectNotFoundException: If project with given ID is not found
        """
        for project in self.projects:
            if project.id == project_id:
                return project

        raise ProjectNotFoundException(f"Project with ID {project_id} not found.")

    def update_project(
        self, project_id: int, name: str = None, description: str = None
    ) -> Project:
        """
        Update an existing project.

        Args:
            project_id (int): ID of the project to update
            name (str, optional): New name for the project
            description (str, optional): New description for the project

        Returns:
            Project: The updated project

        Raises:
            ProjectNotFoundException: If project is not found
            DuplicateProjectException: If new name conflicts with existing project
            ValidationException: If validation fails
        """
        project = self.get_project_by_id(project_id)

        # Validate new name if provided
        if name is not None:
            Validator.validate_project_name(name)
            # Check for duplicate names (excluding current project)
            if name != project.name and self._project_exists_by_name(name):
                raise DuplicateProjectException(
                    f"A project with the name '{name}' already exists."
                )

        # Validate new description if provided
        if description is not None:
            Validator.validate_project_description(description)

        # Update project
        project.update(name=name, description=description)

        return project

    def delete_project(self, project_id: int) -> None:
        """
        Delete a project and all its tasks (cascade delete).

        Args:
            project_id (int): ID of the project to delete

        Raises:
            ProjectNotFoundException: If project is not found
        """
        project = self.get_project_by_id(project_id)
        self.projects.remove(project)

    def _project_exists_by_name(self, name: str) -> bool:
        """
        Check if a project with the given name exists.

        Args:
            name (str): Name to check

        Returns:
            bool: True if project exists, False otherwise
        """
        return any(project.name.lower() == name.lower() for project in self.projects)

    def get_project_count(self) -> int:
        """
        Get the total number of projects.

        Returns:
            int: Number of projects
        """
        return len(self.projects)

    def search_projects(self, search_term: str) -> List[Project]:
        """
        Search projects by name or description.

        Args:
            search_term (str): Term to search for

        Returns:
            List[Project]: List of matching projects
        """
        search_lower = search_term.lower()
        return [
            project
            for project in self.projects
            if search_lower in project.name.lower()
            or search_lower in project.description.lower()
        ]
