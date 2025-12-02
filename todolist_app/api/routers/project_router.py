"""
Project API endpoints.
Provides CRUD operations for projects.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todolist_app.api.dependencies import get_db
from todolist_app.api.schemas.project_schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectRead,
    ProjectList
)
from todolist_app.services.project_service import ProjectService
from todolist_app.exceptions.repository_exceptions import (
    ProjectNotFoundException,
    DuplicateProjectException
)
from todolist_app.exceptions.service_exceptions import (
    ValidationException,
    MaxLimitException
)


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Project not found"}}
)


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new project with name and optional description"
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new project.
    
    - **name**: Project name (required, 1-100 chars)
    - **description**: Project description (optional, max 500 chars)
    """
    service = ProjectService(db)
    
    try:
        created_project = service.create_project(
            name=project.name,
            description=project.description
        )
        return created_project
    except DuplicateProjectException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except MaxLimitException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=ProjectList,
    summary="List all projects",
    description="Retrieve a list of all projects"
)
def list_projects(db: Session = Depends(get_db)):
    """
    Retrieve all projects.
    
    Returns a list of all projects in the system.
    """
    service = ProjectService(db)
    projects = service.list_projects()
    
    return ProjectList(
        projects=projects,
        total=len(projects)
    )


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Get project by ID",
    description="Retrieve a specific project by its ID"
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific project.
    
    - **project_id**: ID of the project to retrieve
    """
    service = ProjectService(db)
    
    try:
        project = service.get_project(project_id)
        return project
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Update a project",
    description="Update project name and/or description"
)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing project.
    
    - **project_id**: ID of the project to update
    - **name**: New project name (optional)
    - **description**: New project description (optional)
    """
    service = ProjectService(db)
    
    try:
        updated_project = service.update_project(
            project_id=project_id,
            name=project.name,
            description=project.description
        )
        return updated_project
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateProjectException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Delete a project and all its tasks (CASCADE)"
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a project.
    
    - **project_id**: ID of the project to delete
    
    Note: This will also delete all tasks associated with this project.
    """
    service = ProjectService(db)
    
    try:
        service.delete_project(project_id)
        return None
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
