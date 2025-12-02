"""
Task API endpoints.
Provides CRUD operations for tasks and status management.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from todolist_app.api.dependencies import get_db
from todolist_app.api.schemas.task_schemas import (
    TaskCreate,
    TaskUpdate,
    TaskRead,
    TaskList,
    TaskStatusUpdate
)
from todolist_app.services.task_service import TaskService
from todolist_app.models.task import TaskStatus
from todolist_app.exceptions.repository_exceptions import (
    TaskNotFoundException,
    ProjectNotFoundException
)
from todolist_app.exceptions.service_exceptions import ValidationException


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}}
)


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task under a specific project"
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    
    - **project_id**: ID of the parent project (required)
    - **title**: Task title (required, 1-200 chars)
    - **description**: Task description (optional, max 1000 chars)
    - **deadline**: Task deadline in ISO 8601 format (optional)
    """
    service = TaskService(db)
    
    try:
        created_task = service.create_task(
            project_id=task.project_id,
            title=task.title,
            description=task.description,
            deadline=task.deadline
        )
        return created_task
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=TaskList,
    summary="List all tasks",
    description="Retrieve all tasks with optional filtering by project or status"
)
def list_tasks(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    status_filter: Optional[TaskStatus] = Query(None, alias="status", description="Filter by task status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks.
    
    Optional query parameters:
    - **project_id**: Filter tasks by project
    - **status**: Filter tasks by status (TODO, IN_PROGRESS, DONE, OVERDUE)
    """
    service = TaskService(db)
    
    # Get all tasks first
    tasks = service.list_tasks()
    
    # Apply filters
    if project_id is not None:
        tasks = [t for t in tasks if t.project_id == project_id]
    
    if status_filter is not None:
        tasks = [t for t in tasks if t.status == status_filter]
    
    return TaskList(
        tasks=tasks,
        total=len(tasks)
    )


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Get task by ID",
    description="Retrieve a specific task by its ID"
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific task.
    
    - **task_id**: ID of the task to retrieve
    """
    service = TaskService(db)
    
    try:
        task = service.get_task(task_id)
        return task
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/{task_id}",
    response_model=TaskRead,
    summary="Update a task",
    description="Update task properties (title, description, deadline, status)"
)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    
    - **task_id**: ID of the task to update
    - **title**: New task title (optional)
    - **description**: New task description (optional)
    - **deadline**: New task deadline (optional)
    - **status**: New task status (optional)
    """
    service = TaskService(db)
    
    try:
        updated_task = service.update_task(
            task_id=task_id,
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            status=task.status.value if task.status else None
        )
        return updated_task
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a specific task"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    
    - **task_id**: ID of the task to delete
    """
    service = TaskService(db)
    
    try:
        service.delete_task(task_id)
        return None
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch(
    "/{task_id}/mark-done",
    response_model=TaskRead,
    summary="Mark task as done",
    description="Mark a task as completed (DONE status)"
)
def mark_task_done(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark a task as done.
    
    - **task_id**: ID of the task to mark as done
    """
    service = TaskService(db)
    
    try:
        updated_task = service.mark_as_done(task_id)
        return updated_task
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch(
    "/{task_id}/mark-overdue",
    response_model=TaskRead,
    summary="Mark task as overdue",
    description="Manually mark a task as overdue"
)
def mark_task_overdue(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark a task as overdue.
    
    - **task_id**: ID of the task to mark as overdue
    """
    service = TaskService(db)
    
    try:
        updated_task = service.mark_as_overdue(task_id)
        return updated_task
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/autoclose-overdue",
    summary="Auto-close overdue tasks",
    description="Automatically close all overdue tasks (sets status to DONE)"
)
def autoclose_overdue_tasks(db: Session = Depends(get_db)):
    """
    Auto-close overdue tasks.
    
    This endpoint triggers the auto-close mechanism for all tasks
    that are past their deadline and not yet marked as done.
    """
    service = TaskService(db)
    closed_count = service.autoclose_overdue_tasks()
    
    return {
        "message": f"Successfully closed {closed_count} overdue task(s)",
        "closed_count": closed_count
    }
