"""
Pydantic models for Task API validation.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from todolist_app.models.task import TaskStatus


class TaskBase(BaseModel):
    """Base schema for task with common fields."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Task description (max 1000 characters)"
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Task deadline (ISO 8601 format)"
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    project_id: int = Field(..., description="ID of the parent project")


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Updated task title"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Updated task description"
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Updated task deadline"
    )
    status: Optional[TaskStatus] = Field(
        None,
        description="Updated task status"
    )


class TaskStatusUpdate(BaseModel):
    """Schema for updating only task status."""
    status: TaskStatus = Field(..., description="New task status")


class TaskRead(TaskBase):
    """Schema for reading task data (response)."""
    id: int = Field(..., description="Task ID")
    project_id: int = Field(..., description="Parent project ID")
    status: TaskStatus = Field(..., description="Current task status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    closed_at: Optional[datetime] = Field(None, description="Task closure timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    """Schema for list of tasks response."""
    tasks: list[TaskRead]
    total: int = Field(..., description="Total number of tasks")
