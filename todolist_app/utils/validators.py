"""
Validators module for the ToDoList application.

This module provides validation functions for user inputs including
word count validation, status validation, and date validation.
"""

from datetime import datetime
from typing import Optional

from todolist_app.exceptions.custom_exceptions import (
    InvalidDateException,
    InvalidStatusException,
    ValidationException,
)
from todolist_app.utils.config import Config


class Validator:
    """
    Validator class containing static methods for input validation.

    This class provides various validation methods to ensure data
    integrity throughout the application.
    """

    @staticmethod
    def validate_word_count(
        text: str, min_words: int, max_words: int, field_name: str
    ) -> None:
        """
        Validate that text contains an acceptable number of words.

        Args:
            text (str): Text to validate
            min_words (int): Minimum number of words required
            max_words (int): Maximum number of words allowed
            field_name (str): Name of the field being validated (for error messages)

        Raises:
            ValidationException: If word count is outside the acceptable range
        """
        if not text or not text.strip():
            raise ValidationException(f"{field_name} cannot be empty.")

        word_count = len(text.split())

        if word_count < min_words:
            raise ValidationException(
                f"{field_name} must contain at least {min_words} words. "
                f"Current: {word_count} words."
            )

        if word_count > max_words:
            raise ValidationException(
                f"{field_name} must not exceed {max_words} words. "
                f"Current: {word_count} words."
            )

    @staticmethod
    def validate_project_name(name: str) -> None:
        """
        Validate project name according to defined rules.

        Args:
            name (str): Project name to validate

        Raises:
            ValidationException: If validation fails
        """
        Validator.validate_word_count(
            name,
            Config.PROJECT_NAME_MIN_WORDS,
            Config.PROJECT_NAME_MAX_WORDS,
            "Project name",
        )

    @staticmethod
    def validate_project_description(description: str) -> None:
        """
        Validate project description according to defined rules.

        Args:
            description (str): Project description to validate

        Raises:
            ValidationException: If validation fails
        """
        Validator.validate_word_count(
            description,
            Config.PROJECT_DESCRIPTION_MIN_WORDS,
            Config.PROJECT_DESCRIPTION_MAX_WORDS,
            "Project description",
        )

    @staticmethod
    def validate_task_title(title: str) -> None:
        """
        Validate task title according to defined rules.

        Args:
            title (str): Task title to validate

        Raises:
            ValidationException: If validation fails
        """
        Validator.validate_word_count(
            title,
            Config.TASK_TITLE_MIN_WORDS,
            Config.TASK_TITLE_MAX_WORDS,
            "Task title",
        )

    @staticmethod
    def validate_task_description(description: str) -> None:
        """
        Validate task description according to defined rules.

        Args:
            description (str): Task description to validate

        Raises:
            ValidationException: If validation fails
        """
        Validator.validate_word_count(
            description,
            Config.TASK_DESCRIPTION_MIN_WORDS,
            Config.TASK_DESCRIPTION_MAX_WORDS,
            "Task description",
        )

    @staticmethod
    def validate_status(status: str) -> None:
        """
        Validate that the provided status is valid.

        Args:
            status (str): Status to validate

        Raises:
            InvalidStatusException: If status is not in the valid statuses list
        """
        valid_statuses = Config.get_valid_statuses()
        if status not in valid_statuses:
            raise InvalidStatusException(
                f"Invalid status: '{status}'. "
                f"Valid statuses are: {', '.join(valid_statuses)}"
            )

    @staticmethod
    def validate_deadline(deadline_str: Optional[str]) -> Optional[datetime]:
        """
        Validate and parse deadline string.

        Args:
            deadline_str (Optional[str]): Deadline string in YYYY-MM-DD format

        Returns:
            Optional[datetime]: Parsed datetime object or None if no deadline

        Raises:
            InvalidDateException: If date format is invalid or date is in the past
        """
        if not deadline_str or deadline_str.strip().lower() in ["none", "", "no"]:
            return None

        try:
            deadline = datetime.strptime(deadline_str.strip(), "%Y-%m-%d")
        except ValueError:
            raise InvalidDateException(
                f"Invalid date format: '{deadline_str}'. "
                f"Please use YYYY-MM-DD format (e.g., 2025-12-31)."
            )

        # Check if deadline is in the future
        if deadline.date() < datetime.now().date():
            raise InvalidDateException(
                f"Deadline cannot be in the past. "
                f"Provided date: {deadline_str}"
            )

        return deadline

    @staticmethod
    def validate_positive_integer(value: str, field_name: str) -> int:
        """
        Validate that a string represents a positive integer.

        Args:
            value (str): String to validate
            field_name (str): Name of the field being validated

        Returns:
            int: Validated integer value

        Raises:
            ValidationException: If value is not a positive integer
        """
        try:
            num = int(value)
            if num <= 0:
                raise ValidationException(
                    f"{field_name} must be a positive integer. Provided: {value}"
                )
            return num
        except ValueError:
            raise ValidationException(
                f"{field_name} must be a valid integer. Provided: {value}"
            )