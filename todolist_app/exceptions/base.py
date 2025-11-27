"""
Base exception classes for ToDoList application.

This module defines the base exception that all other exceptions inherit from.
"""


class TodoListException(Exception):
    """
    Base exception for all ToDoList application errors.
    
    All custom exceptions in the application should inherit from this class.
    """

    def __init__(self, message: str):
        """
        Initialize the exception with a message.
        
        Args:
            message: Error message describing the exception
        """
        self.message = message
        super().__init__(self.message)
