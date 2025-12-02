"""
Pydantic models for Project API validation.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):
    """Base schema for project with common fields."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Project name (1-100 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Project description (max 500 characters)"
    )


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated project name"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Updated project description"
    )


class ProjectRead(ProjectBase):
    """Schema for reading project data (response)."""
    id: int = Field(..., description="Project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class ProjectList(BaseModel):
    """Schema for list of projects response."""
    projects: list[ProjectRead]
    total: int = Field(..., description="Total number of projects")
