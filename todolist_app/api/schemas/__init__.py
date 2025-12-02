from .project_schemas import (
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectRead,
    ProjectInList,
    # Remove ProjectList from here - it's not in the schema file anymore
)

from .task_schemas import (
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskRead,
    TaskInList,
)

__all__ = [
    # Project schemas
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectRead",
    "ProjectInList",
    # Removed "ProjectList"
    
    # Task schemas
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskRead",
    "TaskInList",
]
