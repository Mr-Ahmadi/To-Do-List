"""
Project Service for business logic.

This module handles business logic for project operations,
including validation and coordination between repositories.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from todolist_app.repositories.project_repository import ProjectRepository
from todolist_app.models.project import Project
from todolist_app.exceptions.custom_exceptions import (
    ValidationException,
    MaxLimitException,
)
from todolist_app.utils.validators import Validator
from todolist_app.utils.config import Config


class ProjectService:
    """
    Service class for project business logic.
    
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
        self.repository = ProjectRepository(db)

    def create_project(
        self, 
        name: str, 
        description: Optional[str] = None
    ) -> Project:
        """
        Create a new project with validation.

        Args:
            name (str): Project name (min 1 word, max 30 words)
            description (Optional[str]): Project description (max 150 words)

        Returns:
            Project: Created project

        Raises:
            ValidationException: If validation fails
            DuplicateProjectException: If project name exists
            MaxLimitException: If project limit exceeded
        """
        # Check project limit
        max_projects = Config.get_max_projects()
        if self.repository.count() >= max_projects:
            raise MaxLimitException(
                f"Cannot create project. Maximum {max_projects} projects allowed."
            )

        # Validate inputs
        Validator.validate_project_name(name)
        Validator.validate_project_description(description or "")

        # Create project through repository
        return self.repository.create(name=name, description=description)

    def get_project_by_id(self, project_id: int) -> Project:
        """
        Get project by ID.

        Args:
            project_id (int): Project ID

        Returns:
            Project: Found project

        Raises:
            ProjectNotFoundException: If project not found
        """
        return self.repository.get_by_id(project_id)

    def get_all_projects(self) -> List[Project]:
        """
        Get all projects.

        Returns:
            List[Project]: List of all projects
        """
        return self.repository.get_all()

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Project:
        """
        Update project with validation.

        Args:
            project_id (int): ID of project to update
            name (Optional[str]): New name
            description (Optional[str]): New description

        Returns:
            Project: Updated project

        Raises:
            ProjectNotFoundException: If project not found
            ValidationException: If validation fails
            DuplicateProjectException: If new name exists
        """
        # Validate inputs if provided
        if name is not None:
            Validator.validate_project_name(name)
        
        if description is not None:
            Validator.validate_project_description(description)

        # Update through repository
        return self.repository.update(
            project_id=project_id,
            name=name,
            description=description
        )

    def delete_project(self, project_id: int) -> bool:
        """
        Delete project and all its tasks.

        Args:
            project_id (int): ID of project to delete

        Returns:
            bool: True if deleted successfully

        Raises:
            ProjectNotFoundException: If project not found
        """
        return self.repository.delete(project_id)

    def search_projects(self, query: str) -> List[Project]:
        """
        Search projects by name or description.

        Args:
            query (str): Search term

        Returns:
            List[Project]: List of matching projects
        """
        return self.repository.search(query)

    def get_project_count(self) -> int:
        """
        Get total number of projects.

        Returns:
            int: Number of projects
        """
        return self.repository.count()
