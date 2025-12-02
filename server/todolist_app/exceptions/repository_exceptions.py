"""
Repository layer exceptions for ToDoList application.

This module defines exceptions that are raised by the repository layer
when database operations fail or resources are not found.
"""

from todolist_app.exceptions.base import TodoListException


class DatabaseOperationException(TodoListException):
    """Raised when a database operation fails."""

    pass


class ProjectNotFoundException(TodoListException):
    """Raised when a requested project is not found in the database."""

    pass


class TaskNotFoundException(TodoListException):
    """Raised when a requested task is not found in the database."""

    pass


class DuplicateProjectException(TodoListException):
    """Raised when attempting to create a project with a duplicate name."""

    pass


class DuplicateTaskException(TodoListException):
    """Raised when attempting to create a task with a duplicate title in the same project."""

    pass
