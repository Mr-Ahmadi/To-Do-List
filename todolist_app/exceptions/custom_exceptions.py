"""
Custom exceptions for the ToDoList application.

This module defines all custom exceptions used throughout the application
to handle specific error scenarios.
"""


class TodoListException(Exception):
    """Base exception for all ToDoList application errors."""

    pass


class ValidationException(TodoListException):
    """Raised when input validation fails."""

    pass


class ProjectNotFoundException(TodoListException):
    """Raised when a requested project is not found."""

    pass


class TaskNotFoundException(TodoListException):
    """Raised when a requested task is not found."""

    pass


class DuplicateProjectException(TodoListException):
    """Raised when attempting to create a project with a duplicate name."""

    pass


class MaxLimitException(TodoListException):
    """Raised when maximum limit for projects or tasks is reached."""

    pass


class InvalidStatusException(TodoListException):
    """Raised when an invalid task status is provided."""

    pass


class InvalidDateException(TodoListException):
    """Raised when an invalid date format or past date is provided."""

    pass
