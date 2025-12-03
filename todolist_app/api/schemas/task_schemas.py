from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer
from enum import Enum


# -----------------------------------------------------------
# Status Enum (aligned with Validator)
# -----------------------------------------------------------
class TaskStatus(str, Enum):
    """Task status enumeration"""
    TODO = "todo"
    DOING = "doing" 
    DONE = "done"


# -----------------------------------------------------------
# Base Schema
# -----------------------------------------------------------
class TaskBase(BaseModel):
    """Base schema for Task with common fields"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: Optional[str] = Field(
        None,
        description="Task deadline in YYYY-MM-DD format"
    )
    status: str = Field(default="todo")
    project_id: Optional[int] = Field(None, gt=0)

    @field_validator("deadline", mode="before")
    @classmethod
    def parse_deadline(cls, v):
        """
        Validate and parse deadline.
        Accept: None, datetime object, or YYYY-MM-DD string
        Return: YYYY-MM-DD string or None
        """
        if v is None:
            return None
        
        # If it's already a datetime object, convert to string
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d')
        
        # If it's a string, validate format
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("deadline must be in YYYY-MM-DD format")
        
        raise ValueError("deadline must be a string or datetime object")
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        """Validate status matches allowed values"""
        allowed = ["todo", "doing", "done"]
        if v not in allowed:
            raise ValueError(f"Status must be one of: {', '.join(allowed)}")
        return v


# -----------------------------------------------------------
# Create Schema
# -----------------------------------------------------------
class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    project_id: int = Field(..., gt=0)  # Required for creation
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write API documentation",
                "project_id": 1,
                "deadline": "2025-12-10",
                "status": "todo"
            }
        }


# -----------------------------------------------------------
# Update Schema
# -----------------------------------------------------------
class TaskUpdate(BaseModel):
    """Schema for updating a task - all fields optional"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: Optional[str] = Field(
        None,
        description="Task deadline in YYYY-MM-DD format"
    )
    status: Optional[str] = None
    project_id: Optional[int] = Field(None, gt=0)
    
    @field_validator("deadline", mode="before")
    @classmethod
    def parse_deadline(cls, v):
        """
        Validate and parse deadline for update.
        Accept: None, datetime object, or YYYY-MM-DD string
        Return: YYYY-MM-DD string or None
        """
        if v is None:
            return None
        
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d')
        
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("deadline must be in YYYY-MM-DD format")
        
        raise ValueError("deadline must be a string or datetime object")
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        """Validate status if provided"""
        if v is None:
            return v
        allowed = ["todo", "doing", "done"]
        if v not in allowed:
            raise ValueError(f"Status must be one of: {', '.join(allowed)}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated task title",
                "status": "doing"
            }
        }


# -----------------------------------------------------------
# Read Schema (response)
# -----------------------------------------------------------
class TaskRead(BaseModel):
    """Schema for reading a task from database"""
    id: int
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str
    project_id: int
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('deadline', 'closed_at', when_used='always')
    def serialize_date_only(self, dt: Optional[datetime]) -> Optional[str]:
        """Serialize deadline and closed_at to YYYY-MM-DD format"""
        if dt is None:
            return None
        return dt.strftime('%Y-%m-%d')
    
    @field_serializer('created_at', 'updated_at', when_used='always')
    def serialize_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        """Serialize created_at and updated_at to YYYY-MM-DD HH:MM format"""
        if dt is None:
            return None
        return dt.strftime('%Y-%m-%d %H:%M')


# -----------------------------------------------------------
# List Schema
# -----------------------------------------------------------
class TaskInList(BaseModel):
    """Schema for task in list responses"""
    id: int
    title: str
    status: str
    deadline: Optional[datetime] = None
    project_id: int

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('deadline', when_used='always')
    def serialize_deadline(self, dt: Optional[datetime]) -> Optional[str]:
        """Serialize deadline to YYYY-MM-DD format"""
        if dt is None:
            return None
        return dt.strftime('%Y-%m-%d')
