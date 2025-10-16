class TodoListException(Exception):
    """Base exception class for all project exceptions"""
    pass


class ValidationException(TodoListException):
    """Exception raised for validation errors"""
    pass


class ProjectNotFoundException(TodoListException):
    """Exception raised when a project is not found"""
    pass


class TaskNotFoundException(TodoListException):
    """Exception raised when a task is not found"""
    pass


class DuplicateProjectException(TodoListException):
    """Exception raised when attempting to create a duplicate project name"""
    pass


class MaxLimitException(TodoListException):
    """Exception raised when maximum limit is reached"""
    pass


class InvalidStatusException(TodoListException):
    """Exception raised for invalid task status"""
    pass


class InvalidDateException(TodoListException):
    """Exception raised for invalid date format or value"""
    pass
