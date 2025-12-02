from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Base schema for Task with common fields"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: str = Field(default="pending")
    project_id: Optional[int] = None


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task - all fields optional"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None
    project_id: Optional[int] = None


class TaskRead(TaskBase):
    """Schema for reading a task from database"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskInList(BaseModel):
    """Schema for task in list responses"""
    id: int
    title: str
    status: str
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    project_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
