"""
Validator utilities for the ToDoList application.

This module provides validation functions for various input types
including project names, task titles, descriptions, dates, and statuses.
"""

from datetime import datetime
from typing import Optional

from todolist_app.exceptions.custom_exceptions import (
    InvalidDateException,
    InvalidStatusException,
    ValidationException,
)


class Validator:
    """Validator class for input validation."""

    # Valid task statuses
    VALID_STATUSES = ["todo", "doing", "done"]

    # Word limits
    MAX_NAME_WORDS = 30
    MIN_NAME_WORDS = 1  # ✅ Minimum 1 word for names
    MAX_DESCRIPTION_WORDS = 150

    @staticmethod
    def validate_project_name(name: str) -> None:
        """
        Validate project name.

        Args:
            name (str): Project name to validate

        Raises:
            ValidationException: If validation fails
        """
        if not name or not name.strip():
            raise ValidationException("Project name cannot be empty.")

        word_count = len(name.strip().split())
        
        if word_count < Validator.MIN_NAME_WORDS:
            raise ValidationException(
                f"Project name must contain at least {Validator.MIN_NAME_WORDS} word."
            )

        if word_count > Validator.MAX_NAME_WORDS:
            raise ValidationException(
                f"Project name cannot exceed {Validator.MAX_NAME_WORDS} words. "
                f"Current: {word_count} words."
            )

    @staticmethod
    def validate_project_description(description: str) -> None:
        """
        Validate project description.

        Args:
            description (str): Project description to validate

        Raises:
            ValidationException: If validation fails
        """
        # ✅ Description is optional - empty string is valid
        if description is None:
            return

        # If provided, check word limit
        if description.strip():
            word_count = len(description.strip().split())
            if word_count > Validator.MAX_DESCRIPTION_WORDS:
                raise ValidationException(
                    f"Project description cannot exceed {Validator.MAX_DESCRIPTION_WORDS} words. "
                    f"Current: {word_count} words."
                )

    @staticmethod
    def validate_task_title(title: str) -> None:
        """
        Validate task title.

        Args:
            title (str): Task title to validate

        Raises:
            ValidationException: If validation fails
        """
        if not title or not title.strip():
            raise ValidationException("Task title cannot be empty.")

        word_count = len(title.strip().split())
        
        if word_count < Validator.MIN_NAME_WORDS:
            raise ValidationException(
                f"Task title must contain at least {Validator.MIN_NAME_WORDS} word."
            )

        if word_count > Validator.MAX_NAME_WORDS:
            raise ValidationException(
                f"Task title cannot exceed {Validator.MAX_NAME_WORDS} words. "
                f"Current: {word_count} words."
            )

    @staticmethod
    def validate_task_description(description: str) -> None:
        """
        Validate task description.

        Args:
            description (str): Task description to validate

        Raises:
            ValidationException: If validation fails
        """
        # ✅ Task description is still required
        if not description or not description.strip():
            raise ValidationException("Task description cannot be empty.")

        word_count = len(description.strip().split())

        if word_count > Validator.MAX_DESCRIPTION_WORDS:
            raise ValidationException(
                f"Task description cannot exceed {Validator.MAX_DESCRIPTION_WORDS} words. "
                f"Current: {word_count} words."
            )

    @staticmethod
    def validate_status(status: str) -> None:
        """
        Validate task status.

        Args:
            status (str): Status to validate

        Raises:
            InvalidStatusException: If status is invalid
        """
        if status not in Validator.VALID_STATUSES:
            raise InvalidStatusException(
                f"Invalid status: '{status}'. "
                f"Valid statuses are: {', '.join(Validator.VALID_STATUSES)}"
            )

    @staticmethod
    def validate_deadline(deadline: Optional[str]) -> Optional[datetime]:
        """
        Validate and parse deadline string.

        Args:
            deadline (Optional[str]): Deadline string in YYYY-MM-DD format

        Returns:
            Optional[datetime]: Parsed datetime object or None

        Raises:
            InvalidDateException: If date format is invalid
        """
        if deadline is None or deadline.strip() == "":
            return None

        try:
            # Parse the date string
            deadline_dt = datetime.strptime(deadline.strip(), "%Y-%m-%d")
            return deadline_dt
        except ValueError:
            raise InvalidDateException(
                f"Invalid date format: '{deadline}'. "
                f"Expected format: YYYY-MM-DD (e.g., 2024-12-31)"
            )

    @staticmethod
    def validate_id(entity_id: int, entity_type: str = "entity") -> None:
        """
        Validate entity ID.

        Args:
            entity_id (int): ID to validate
            entity_type (str): Type of entity for error message

        Raises:
            ValidationException: If ID is invalid
        """
        if not isinstance(entity_id, int):
            raise ValidationException(
                f"{entity_type.capitalize()} ID must be an integer."
            )

        if entity_id < 1:
            raise ValidationException(
                f"{entity_type.capitalize()} ID must be a positive integer."
            )
