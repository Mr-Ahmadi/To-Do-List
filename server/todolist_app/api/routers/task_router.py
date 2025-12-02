from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from todolist_app.api.dependencies import get_db
from todolist_app.services.task_service import TaskService
from todolist_app.services.project_service import ProjectService

from todolist_app.api.schemas.task_schemas import (
    TaskCreate,
    TaskUpdate,
    TaskRead,
    TaskInList,
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    
    - **title**: Task title (required)
    - **description**: Task description (required)
    - **project_id**: ID of parent project (required)
    - **due_date**: Deadline in YYYY-MM-DD format (optional)
    - **status**: Initial status (default: 'todo')
    - **priority**: Task priority (optional)
    """
    task_service = TaskService(db)
    
    # Validate project_id - it's required in the service
    if not task_data.project_id:
        raise HTTPException(status_code=400, detail="project_id is required")
    
    project_service = ProjectService(db)
    project = project_service.get_project_by_id(task_data.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Service expects: project_id, title, description, deadline (not due_date), status
        task = task_service.create_task(
            project_id=task_data.project_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.due_date.isoformat() if task_data.due_date else None,
            status=task_data.status if task_data.status else "todo"
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TaskInList])
def list_tasks(
    project_id: Optional[int] = Query(None, description="Filter tasks by project ID"),
    status: Optional[str] = Query(None, description="Filter tasks by status (todo, in_progress, done, overdue)"),
    db: Session = Depends(get_db)
):
    """
    List all tasks with optional filters.
    
    - **project_id**: Filter by project (optional)
    - **status**: Filter by status (optional)
    """
    task_service = TaskService(db)
    
    try:
        if project_id and status:
            # Filter by both project and status
            tasks = task_service.get_tasks_by_status(project_id, status)
        elif project_id:
            # Filter by project only
            tasks = task_service.get_tasks_by_project(project_id)
        elif status:
            # Status filter without project not directly supported
            # We'd need to get all tasks first - service doesn't have get_all_tasks()
            raise HTTPException(
                status_code=400, 
                detail="Status filter requires project_id"
            )
        else:
            # No filters - but service doesn't have get_all_tasks()
            raise HTTPException(
                status_code=400,
                detail="Please provide project_id to list tasks"
            )
        
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/overdue", response_model=List[TaskInList])
def list_overdue_tasks(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    db: Session = Depends(get_db)
):
    """
    Get all overdue tasks.
    
    - **project_id**: Filter by project (optional)
    """
    task_service = TaskService(db)
    tasks = task_service.get_overdue_tasks(project_id)
    return tasks


@router.get("/search", response_model=List[TaskInList])
def search_tasks(
    project_id: int = Query(..., description="Project ID to search within"),
    query: str = Query(..., description="Search term"),
    db: Session = Depends(get_db)
):
    """
    Search tasks by title or description.
    
    - **project_id**: Project to search in (required)
    - **query**: Search term (required)
    """
    task_service = TaskService(db)
    tasks = task_service.search_tasks(project_id, query)
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.
    
    - **task_id**: ID of the task
    """
    task_service = TaskService(db)
    
    try:
        task = task_service.get_task_by_id(task_id)
        return task
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a task.
    
    All fields are optional - only provided fields will be updated.
    
    - **title**: New task title
    - **description**: New description
    - **due_date**: New deadline in YYYY-MM-DD format
    - **status**: New status (todo, in_progress, done, overdue)
    """
    task_service = TaskService(db)
    
    # Check if task exists
    try:
        task = task_service.get_task_by_id(task_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Validate project_id if being updated
    if task_data.project_id:
        project_service = ProjectService(db)
        try:
            project = project_service.get_project_by_id(task_data.project_id)
        except Exception:
            raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Service expects: task_id, title, description, deadline (not due_date), status
        updated_task = task_service.update_task(
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.due_date.isoformat() if task_data.due_date else None,
            status=task_data.status
        )
        return updated_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{task_id}/mark-done", response_model=TaskRead)
def mark_task_done(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark a task as done.
    
    - **task_id**: ID of the task
    """
    task_service = TaskService(db)
    
    try:
        task = task_service.mark_task_as_done(task_id)
        return task
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    
    - **task_id**: ID of the task to delete
    """
    task_service = TaskService(db)
    
    try:
        task_service.get_task_by_id(task_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_service.delete_task(task_id)
    return None
