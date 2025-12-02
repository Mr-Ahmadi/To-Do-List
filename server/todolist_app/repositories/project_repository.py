"""
Project Repository for database operations.

This module handles all database queries related to Project entities.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from todolist_app.models.project import Project
from todolist_app.exceptions.repository_exceptions import (
    ProjectNotFoundException,
    DuplicateProjectException,
    DatabaseOperationException,
)


class ProjectRepository:
    """
    Repository class for Project database operations.
    
    This class follows the Repository pattern and handles all
    database interactions for Project entities using SQLAlchemy ORM.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with database session.

        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db

    def create(self, name: str, description: Optional[str] = None) -> Project:
        """
        Create a new project in database.

        Args:
            name (str): Project name (must be unique)
            description (Optional[str]): Project description

        Returns:
            Project: Created project with generated ID

        Raises:
            DuplicateProjectException: If project with same name exists
            DatabaseOperationException: If database operation fails
        """
        try:
            # Check if project with same name exists
            existing = self.db.query(Project).filter(
                Project.name == name
            ).first()
            
            if existing:
                raise DuplicateProjectException(
                    f"Project with name '{name}' already exists."
                )

            # Create new project
            project = Project(
                name=name,
                description=description or ""
            )
            
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            
            return project
            
        except DuplicateProjectException:
            raise
        except IntegrityError as e:
            self.db.rollback()
            raise DuplicateProjectException(
                f"Project with name '{name}' already exists."
            )
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationException(
                f"Failed to create project: {str(e)}"
            )

    def get_by_id(self, project_id: int) -> Project:
        """
        Get project by ID.

        Args:
            project_id (int): Project ID to search for

        Returns:
            Project: Found project

        Raises:
            ProjectNotFoundException: If project not found
        """
        project = self.db.query(Project).filter(
            Project.id == project_id
        ).first()
        
        if not project:
            raise ProjectNotFoundException(
                f"Project with ID {project_id} not found."
            )
        
        return project

    def get_by_name(self, name: str) -> Optional[Project]:
        """
        Get project by name.

        Args:
            name (str): Project name to search for

        Returns:
            Optional[Project]: Found project or None
        """
        return self.db.query(Project).filter(
            Project.name == name
        ).first()

    def get_all(self) -> List[Project]:
        """
        Get all projects ordered by creation date.

        Returns:
            List[Project]: List of all projects
        """
        return self.db.query(Project).order_by(
            Project.created_at.desc()
        ).all()

    def update(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Project:
        """
        Update project information.

        Args:
            project_id (int): ID of project to update
            name (Optional[str]): New name (if provided)
            description (Optional[str]): New description (if provided)

        Returns:
            Project: Updated project

        Raises:
            ProjectNotFoundException: If project not found
            DuplicateProjectException: If new name already exists
            DatabaseOperationException: If update fails
        """
        try:
            project = self.get_by_id(project_id)

            # Check for duplicate name if name is being updated
            if name is not None and name != project.name:
                existing = self.get_by_name(name)
                if existing:
                    raise DuplicateProjectException(
                        f"Project with name '{name}' already exists."
                    )
                project.name = name

            # Update description if provided
            if description is not None:
                project.description = description

            self.db.commit()
            self.db.refresh(project)
            
            return project
            
        except (ProjectNotFoundException, DuplicateProjectException):
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationException(
                f"Failed to update project: {str(e)}"
            )

    def delete(self, project_id: int) -> bool:
        """
        Delete project from database.
        
        Note: This will also delete all associated tasks due to CASCADE.

        Args:
            project_id (int): ID of project to delete

        Returns:
            bool: True if deleted successfully

        Raises:
            ProjectNotFoundException: If project not found
            DatabaseOperationException: If deletion fails
        """
        try:
            project = self.get_by_id(project_id)
            
            self.db.delete(project)
            self.db.commit()
            
            return True
            
        except ProjectNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationException(
                f"Failed to delete project: {str(e)}"
            )

    def search(self, query: str) -> List[Project]:
        """
        Search projects by name or description.

        Args:
            query (str): Search term

        Returns:
            List[Project]: List of matching projects
        """
        search_pattern = f"%{query}%"
        return self.db.query(Project).filter(
            (Project.name.ilike(search_pattern)) |
            (Project.description.ilike(search_pattern))
        ).order_by(Project.created_at.desc()).all()

    def count(self) -> int:
        """
        Get total number of projects.

        Returns:
            int: Number of projects
        """
        return self.db.query(Project).count()
