"""
ToDoList Application
A command-line To-Do List application built with Python OOP.
"""

__version__ = "0.1.0"
__author__ = "Ali Ahmadi"
__email__ = "mr-ahmadi2004@outlook.com"

from todolist_app.exceptions.custom_exceptions import (
    DuplicateProjectException,
    InvalidDateException,
    InvalidStatusException,
    MaxLimitException,
    ProjectNotFoundException,
    TaskNotFoundException,
    TodoListException,
    ValidationException,
)
from todolist_app.managers.project_manager import ProjectManager
from todolist_app.managers.task_manager import TaskManager
from todolist_app.models.project import Project
from todolist_app.models.task import Task

__all__ = [
    "__version__",
    "TodoListException",
    "ValidationException",
    "ProjectNotFoundException",
    "TaskNotFoundException",
    "DuplicateProjectException",
    "MaxLimitException",
    "InvalidStatusException",
    "InvalidDateException",
    "Project",
    "Task",
    "ProjectManager",
    "TaskManager",
]
