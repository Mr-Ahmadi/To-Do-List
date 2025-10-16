"""
Configuration module for the ToDoList application.

This module loads and manages application configuration from environment
variables using python-dotenv.
"""

import os
from typing import List

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class for managing application settings.

    This class loads configuration values from environment variables
    and provides default values when environment variables are not set.
    """

    # Maximum limits
    MAX_NUMBER_OF_PROJECT: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
    MAX_NUMBER_OF_TASK: int = int(os.getenv("MAX_NUMBER_OF_TASK", "50"))

    # Word count limits for validation
    PROJECT_NAME_MIN_WORDS: int = 2
    PROJECT_NAME_MAX_WORDS: int = 4
    PROJECT_DESCRIPTION_MIN_WORDS: int = 5
    PROJECT_DESCRIPTION_MAX_WORDS: int = 30

    TASK_TITLE_MIN_WORDS: int = 2
    TASK_TITLE_MAX_WORDS: int = 8
    TASK_DESCRIPTION_MIN_WORDS: int = 5
    TASK_DESCRIPTION_MAX_WORDS: int = 50

    # Valid task statuses
    VALID_STATUSES: List[str] = ["todo", "in_progress", "done"]

    # Application settings
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    @classmethod
    def get_max_projects(cls) -> int:
        """
        Get maximum number of projects allowed.

        Returns:
            int: Maximum number of projects
        """
        return cls.MAX_NUMBER_OF_PROJECT

    @classmethod
    def get_max_tasks(cls) -> int:
        """
        Get maximum number of tasks allowed per project.

        Returns:
            int: Maximum number of tasks
        """
        return cls.MAX_NUMBER_OF_TASK

    @classmethod
    def get_valid_statuses(cls) -> List[str]:
        """
        Get list of valid task statuses.

        Returns:
            List[str]: List of valid status values
        """
        return cls.VALID_STATUSES

    @classmethod
    def is_debug_mode(cls) -> bool:
        """
        Check if application is in debug mode.

        Returns:
            bool: True if debug mode is enabled
        """
        return cls.DEBUG

    @classmethod
    def get_environment(cls) -> str:
        """
        Get current application environment.

        Returns:
            str: Current environment (development/production/testing)
        """
        return cls.APP_ENV
