from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from todolist_app.api.dependencies import get_db
from todolist_app.api.schemas.project_schemas import (
    ProjectCreate, 
    ProjectUpdate, 
    ProjectRead, 
    ProjectInList
)
from todolist_app.services.project_service import ProjectService
from todolist_app.exceptions import ProjectNotFoundException

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    service = ProjectService(db)
    created = service.create_project(
        name=project.name,  # Changed from title to name
        description=project.description
    )
    return created


@router.get("/", response_model=List[ProjectInList])
def list_projects(db: Session = Depends(get_db)):
    """List all projects"""
    service = ProjectService(db)
    projects = service.get_all_projects()
    return projects


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project by ID"""
    service = ProjectService(db)
    try:
        project = service.get_project_by_id(project_id)
        return project
    except ProjectNotFoundException:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    """Update a project"""
    service = ProjectService(db)
    try:
        updated = service.update_project(
            project_id=project_id,
            name=project.name,  # Changed from title to name
            description=project.description
        )
        return updated
    except ProjectNotFoundException:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project"""
    service = ProjectService(db)
    try:
        service.delete_project(project_id)
        return None
    except ProjectNotFoundException:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")
