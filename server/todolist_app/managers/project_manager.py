"""Project manager for handling project operations."""
from typing import List, Optional
from todolist_app.models.project import Project
from todolist_app.exceptions.custom_exceptions import (
    ValidationException,
    DuplicateProjectException,
    ProjectNotFoundException,
    MaxLimitException,
)
from todolist_app.utils.validators import Validator
from todolist_app.utils.config import Config


class ProjectManager:
    """Manager class for project operations."""

    _next_id: int = 1  # ✅ Class variable for persistent IDs
    
    def __init__(self):
        """Initialize project manager."""
        self.projects: List[Project] = []

    @classmethod
    def _get_next_id(cls) -> int:
        """
        Get next available project ID.

        Returns:
            int: Next project ID
        """
        current_id = cls._next_id
        cls._next_id += 1
        return current_id

    @classmethod
    def reset_id_counter(cls) -> None:
        """Reset the project ID counter (useful for testing)."""
        cls._next_id = 1

    def _is_duplicate_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if project name already exists.

        Args:
            name (str): Project name to check
            exclude_id (Optional[int]): Project ID to exclude from check (for updates)

        Returns:
            bool: True if name exists, False otherwise
        """
        for project in self.projects:
            if exclude_id and project.id == exclude_id:
                continue
            if project.name.lower() == name.lower():
                return True
        return False

    def create_project(
        self, name: str, description: Optional[str] = None
    ) -> Project:
        """
        Create a new project.

        Args:
            name (str): Project name (min 1 word, max 30 words)
            description (Optional[str]): Project description (optional, max 150 words)

        Returns:
            Project: Created project

        Raises:
            ValidationException: If validation fails
            DuplicateProjectException: If project name already exists
            MaxLimitException: If project limit is exceeded
        """
        # Check project limit
        max_projects = Config.get_max_projects()
        if len(self.projects) >= max_projects:
            raise MaxLimitException(
                f"Cannot create project. Maximum {max_projects} projects allowed."
            )

        # Validate inputs
        Validator.validate_project_name(name)
        Validator.validate_project_description(description or "")  # ✅ Allow empty

        # Check for duplicate name
        if self._is_duplicate_name(name):
            raise DuplicateProjectException(
                f"Project with name '{name}' already exists."
            )

        # Create project with unique ID
        project = Project(
            id=self._get_next_id(),
            name=name,
            description=description or "",  # ✅ Default to empty string
        )

        self.projects.append(project)
        return project

    def get_project_by_id(self, project_id: int) -> Project:
        """
        Get project by ID.

        Args:
            project_id (int): Project ID to search for

        Returns:
            Project: Project if found

        Raises:
            ProjectNotFoundException: If project is not found
        """
        for project in self.projects:
            if project.id == project_id:
                return project
        
        raise ProjectNotFoundException(f"Project with ID {project_id} not found.")

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        """
        Update an existing project.

        Args:
            project_id (int): ID of project to update
            name (Optional[str]): New name (optional)
            description (Optional[str]): New description (optional)

        Returns:
            Project: Updated project

        Raises:
            ProjectNotFoundException: If project is not found
            ValidationException: If validation fails
            DuplicateProjectException: If new name already exists
        """
        project = self.get_project_by_id(project_id)

        # Validate and update name if provided
        if name is not None:
            Validator.validate_project_name(name)
            if self._is_duplicate_name(name, exclude_id=project_id):
                raise DuplicateProjectException(
                    f"Project with name '{name}' already exists."
                )
            project.name = name

        # Validate and update description if provided
        if description is not None:
            Validator.validate_project_description(description)
            project.description = description

        return project

    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project by ID.

        Args:
            project_id (int): ID of project to delete

        Returns:
            bool: True if project was deleted

        Raises:
            ProjectNotFoundException: If project is not found
        """
        project = self.get_project_by_id(project_id)
        self.projects.remove(project)
        return True

    def get_all_projects(self) -> List[Project]:
        """
        Get all projects sorted by creation date.

        Returns:
            List[Project]: List of all projects
        """
        return sorted(self.projects, key=lambda p: p.created_at)

    def search_projects(self, query: str) -> List[Project]:
        """
        Search projects by name or description.

        Args:
            query (str): Search query string

        Returns:
            List[Project]: List of projects matching the query
        """
        query_lower = query.lower()
        return [
            project
            for project in self.projects
            if query_lower in project.name.lower()
            or query_lower in project.description.lower()
        ]