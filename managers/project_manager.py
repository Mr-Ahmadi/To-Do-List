# managers/project_manager.py

from typing import List, Optional
from models.project import Project
from models.task import Task
from utils.config import Config
from utils.validators import Validator
from exceptions import (
    ProjectNotFoundException,
    DuplicateProjectException,
    MaxLimitException
)


class ProjectManager:
    """Manager class for handling project-related operations"""
    
    def __init__(self):
        """Initialize ProjectManager with an empty project list"""
        self.projects: List[Project] = []
    
    def create_project(self, name: str, description: str) -> Project:
        """
        Create a new project.
        
        Args:
            name: Project name
            description: Project description
        
        Returns:
            The created Project instance
        
        Raises:
            ValidationException: If validation fails
            DuplicateProjectException: If project name already exists
            MaxLimitException: If maximum project limit reached
        """
        # Validate inputs
        Validator.validate_project_name(name)
        Validator.validate_project_description(description)
        
        # Check for maximum limit
        if len(self.projects) >= Config.MAX_NUMBER_OF_PROJECT:
            raise MaxLimitException(
                f"Maximum number of projects ({Config.MAX_NUMBER_OF_PROJECT}) reached. "
                "Cannot create more projects."
            )
        
        # Check for duplicate names
        if self._project_exists(name):
            raise DuplicateProjectException(
                f"A project with the name '{name}' already exists."
            )
        
        # Create and add the project
        project = Project(name=name, description=description)
        self.projects.append(project)
        return project
    
    def get_project(self, project_id: int) -> Project:
        """
        Get a project by its ID.
        
        Args:
            project_id: ID of the project to retrieve
        
        Returns:
            The Project instance
        
        Raises:
            ProjectNotFoundException: If project is not found
        """
        for project in self.projects:
            if project.id == project_id:
                return project
        
        raise ProjectNotFoundException(
            f"Project with ID {project_id} not found."
        )
    
    def list_projects(self) -> List[Project]:
        """
        Get all projects.
        
        Returns:
            List of all Project instances
        """
        return self.projects
    
    def update_project(
        self, 
        project_id: int, 
        name: Optional[str] = None, 
        description: Optional[str] = None
    ) -> Project:
        """
        Update a project's details.
        
        Args:
            project_id: ID of the project to update
            name: New project name (optional)
            description: New project description (optional)
        
        Returns:
            The updated Project instance
        
        Raises:
            ProjectNotFoundException: If project is not found
            ValidationException: If validation fails
            DuplicateProjectException: If new name already exists
        """
        project = self.get_project(project_id)
        
        # Validate new name if provided
        if name:
            Validator.validate_project_name(name)
            # Check for duplicate names (excluding current project)
            if name != project.name and self._project_exists(name):
                raise DuplicateProjectException(
                    f"A project with the name '{name}' already exists."
                )
        
        # Validate new description if provided
        if description:
            Validator.validate_project_description(description)
        
        # Update the project
        project.update(name=name, description=description)
        return project
    
    def delete_project(self, project_id: int) -> None:
        """
        Delete a project and all its tasks (cascade delete).
        
        Args:
            project_id: ID of the project to delete
        
        Raises:
            ProjectNotFoundException: If project is not found
        """
        project = self.get_project(project_id)
        self.projects.remove(project)
    
    def _project_exists(self, name: str) -> bool:
        """
        Check if a project with the given name exists.
        
        Args:
            name: Project name to check
        
        Returns:
            True if project exists, False otherwise
        """
        return any(p.name.lower() == name.lower() for p in self.projects)
    
    def get_total_tasks_count(self) -> int:
        """
        Get total number of tasks across all projects.
        
        Returns:
            Total task count
        """
        return sum(len(project.tasks) for project in self.projects)
    
    def __repr__(self) -> str:
        return f"ProjectManager(projects={len(self.projects)})"
