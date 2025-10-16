from datetime import datetime
from typing import Optional
from exceptions import (
    ValidationException,
    InvalidStatusException,
    InvalidDateException
)
from utils.config import Config


class Validator:
    """Input validation utility class"""
    
    @staticmethod
    def validate_word_count(text: str, max_words: int, field_name: str) -> None:
        """
        Validate the word count of a text field.
        
        Args:
            text: The input text to validate
            max_words: Maximum allowed word count
            field_name: Name of the field (for error messages)
        
        Raises:
            ValidationException: If validation fails
        """
        if not text or not text.strip():
            raise ValidationException(f"{field_name} cannot be empty.")
        
        word_count = len(text.split())
        if word_count > max_words:
            raise ValidationException(
                f"{field_name} must not exceed {max_words} words. "
                f"Current word count: {word_count}"
            )
    
    @staticmethod
    def validate_project_name(name: str) -> None:
        """
        Validate project name.
        
        Args:
            name: Project name to validate
        
        Raises:
            ValidationException: If validation fails
        """
        Validator.validate_word_count(
            name,
            Config.PROJECT_NAME_MAX_WORDS,
            "Project name"
        )
    
    @staticmethod
    def validate_project_description(description: str) -> None:
        """
        Validate project description.
        
        Args:
            description: Project description to validate
        
        Raises:
            ValidationException: If validation fails
        """
        Validator.validate_word_count(
            description,
            Config.PROJECT_DESCRIPTION_MAX_WORDS,
            "Project description"
        )
    
    @staticmethod
    def validate_task_title(title: str) -> None:
        """
        Validate task title.
        
        Args:
            title: Task title to validate
        
        Raises:
            ValidationException: If validation fails
        """
        Validator.validate_word_count(
            title,
            Config.TASK_TITLE_MAX_WORDS,
            "Task title"
        )
    
    @staticmethod
    def validate_task_description(description: str) -> None:
        """
        Validate task description.
        
        Args:
            description: Task description to validate
        
        Raises:
            ValidationException: If validation fails
        """
        Validator.validate_word_count(
            description,
            Config.TASK_DESCRIPTION_MAX_WORDS,
            "Task description"
        )
    
    @staticmethod
    def validate_status(status: str) -> None:
        """
        Validate task status.
        
        Args:
            status: Task status to validate
        
        Raises:
            InvalidStatusException: If status is invalid
        """
        if status not in Config.VALID_STATUSES:
            raise InvalidStatusException(
                f"Invalid status. Valid statuses are: "
                f"{', '.join(Config.VALID_STATUSES)}"
            )
    
    @staticmethod
    def validate_deadline(deadline: Optional[str]) -> Optional[datetime]:
        """
        Validate and convert deadline string to datetime object.
        
        Args:
            deadline: Date string in format 'YYYY-MM-DD' or None
        
        Returns:
            datetime object or None
        
        Raises:
            InvalidDateException: If date format is invalid or date is in the past
        """
        if deadline is None or deadline.strip() == "":
            return None
        
        try:
            # Parse the date
            parsed_date = datetime.strptime(deadline.strip(), Config.DATE_FORMAT)
            
            # Check if date is not in the past
            if parsed_date.date() < datetime.now().date():
                raise InvalidDateException(
                    "Deadline cannot be in the past."
                )
            
            return parsed_date
        except ValueError:
            raise InvalidDateException(
                f"Invalid date format. Expected format: {Config.DATE_FORMAT} "
                f"(example: 2025-12-31)"
            )
    
    @staticmethod
    def validate_non_empty(value: str, field_name: str) -> None:
        """
        Validate that a field is not empty.
        
        Args:
            value: Value to validate
            field_name: Name of the field
        
        Raises:
            ValidationException: If field is empty
        """
        if not value or not value.strip():
            raise ValidationException(f"{field_name} cannot be empty.")
