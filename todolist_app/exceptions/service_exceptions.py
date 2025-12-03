"""
Service layer exceptions for ToDoList application.

This module defines exceptions that are raised by the service layer
when business logic validation fails or constraints are violated.
"""

from todolist_app.exceptions.base import TodoListException


class ValidationException(TodoListException):
    """
    Base class for all validation-related exceptions.
    
    Raised when input validation fails at the service layer.
    """

    pass


class InvalidNameException(ValidationException):
    """Raised when a project or task name fails validation."""

    pass


class InvalidDescriptionException(ValidationException):
    """Raised when a description fails validation."""

    pass


class InvalidTitleException(ValidationException):
    """Raised when a task title fails validation."""

    pass


class InvalidDateException(ValidationException):
    """Raised when an invalid date format or past date is provided."""

    pass


class InvalidStatusException(ValidationException):
    """Raised when an invalid task status is provided."""

    pass


class MaxLimitException(TodoListException):
    """
    Raised when maximum limit for resources is reached.
    
    This includes limits on number of projects or tasks.
    """

    pass


class BusinessRuleViolationException(TodoListException):
    """Raised when a business rule is violated."""

    pass
