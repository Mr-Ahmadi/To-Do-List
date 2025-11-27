"""
Custom exceptions package for ToDoList application.

This package organizes exceptions by their layer:
- base: Base exception class
- repository_exceptions: Database/repository layer exceptions
- service_exceptions: Business logic/service layer exceptions
"""

from todolist_app.exceptions.base import TodoListException

# Repository layer exceptions
from todolist_app.exceptions.repository_exceptions import (
    DatabaseOperationException,
    DuplicateProjectException,
    DuplicateTaskException,
    ProjectNotFoundException,
    TaskNotFoundException,
)

# Service layer exceptions
from todolist_app.exceptions.service_exceptions import (
    BusinessRuleViolationException,
    InvalidDateException,
    InvalidDescriptionException,
    InvalidNameException,
    InvalidStatusException,
    InvalidTitleException,
    MaxLimitException,
    ValidationException,
)

__all__ = [
    # Base
    "TodoListException",
    # Repository exceptions
    "DatabaseOperationException",
    "ProjectNotFoundException",
    "TaskNotFoundException",
    "DuplicateProjectException",
    "DuplicateTaskException",
    # Service exceptions
    "ValidationException",
    "InvalidNameException",
    "InvalidDescriptionException",
    "InvalidTitleException",
    "InvalidDateException",
    "InvalidStatusException",
    "MaxLimitException",
    "BusinessRuleViolationException",
]
