from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base schema for Project"""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class ProjectRead(ProjectBase):
    """Schema for reading a project (response)"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProjectInList(BaseModel):
    """Schema for project in list view"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
