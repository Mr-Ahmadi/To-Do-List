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

    # ========== Database Configuration ==========
    DB_USER: str = os.getenv("DB_USER", "todouser")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "todopass")
    DB_NAME: str = os.getenv("DB_NAME", "todolist_db")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    # ========== Application Settings ==========
    APP_NAME: str = os.getenv("APP_NAME", "ToDoList")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # ========== Maximum Limits ==========
    MAX_NUMBER_OF_PROJECT: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
    MAX_NUMBER_OF_TASK: int = int(os.getenv("MAX_NUMBER_OF_TASK", "50"))

    # ========== Word Count Limits for Validation ==========
    # Project validation
    PROJECT_NAME_MIN_WORDS: int = 1
    PROJECT_NAME_MAX_WORDS: int = 30
    PROJECT_DESCRIPTION_MIN_WORDS: int = 0  # Optional
    PROJECT_DESCRIPTION_MAX_WORDS: int = 150

    # Task validation
    TASK_TITLE_MIN_WORDS: int = 1
    TASK_TITLE_MAX_WORDS: int = 30
    TASK_DESCRIPTION_MIN_WORDS: int = 1
    TASK_DESCRIPTION_MAX_WORDS: int = 150

    # Valid task statuses (from PDF: todo | doing | done)
    VALID_STATUSES: List[str] = ["todo", "doing", "done"]

    # ========== Database Methods ==========
    @classmethod
    def get_database_url(cls, sync: bool = True) -> str:
        """
        Get PostgreSQL database connection URL.

        Args:
            sync (bool): If True, returns synchronous URL (postgresql://)
                        If False, returns async URL (postgresql+asyncpg://)

        Returns:
            str: Database connection URL

        Examples:
            >>> Config.get_database_url()
            'postgresql://todouser:todopass@localhost:5432/todolist_db'
            >>> Config.get_database_url(sync=False)
            'postgresql+asyncpg://todouser:todopass@localhost:5432/todolist_db'
        """
        # Check if DATABASE_URL is explicitly set
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return database_url

        # Construct from individual components
        driver = "postgresql" if sync else "postgresql+asyncpg"
        return (
            f"{driver}://{cls.DB_USER}:{cls.DB_PASSWORD}"
            f"@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )

    @classmethod
    def get_database_config(cls) -> dict:
        """
        Get database configuration as dictionary.

        Returns:
            dict: Dictionary containing all database configuration parameters
        """
        return {
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "database": cls.DB_NAME,
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
        }

    # ========== Application Methods ==========
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

    @classmethod
    def get_app_name(cls) -> str:
        """
        Get application name.

        Returns:
            str: Application name
        """
        return cls.APP_NAME

    # ========== Validation Limit Methods ==========
    @classmethod
    def get_project_name_limits(cls) -> tuple[int, int]:
        """
        Get project name word limits.

        Returns:
            tuple[int, int]: (min_words, max_words)
        """
        return (cls.PROJECT_NAME_MIN_WORDS, cls.PROJECT_NAME_MAX_WORDS)

    @classmethod
    def get_project_description_limits(cls) -> tuple[int, int]:
        """
        Get project description word limits.

        Returns:
            tuple[int, int]: (min_words, max_words)
        """
        return (
            cls.PROJECT_DESCRIPTION_MIN_WORDS,
            cls.PROJECT_DESCRIPTION_MAX_WORDS,
        )

    @classmethod
    def get_task_title_limits(cls) -> tuple[int, int]:
        """
        Get task title word limits.

        Returns:
            tuple[int, int]: (min_words, max_words)
        """
        return (cls.TASK_TITLE_MIN_WORDS, cls.TASK_TITLE_MAX_WORDS)

    @classmethod
    def get_task_description_limits(cls) -> tuple[int, int]:
        """
        Get task description word limits.

        Returns:
            tuple[int, int]: (min_words, max_words)
        """
        return (
            cls.TASK_DESCRIPTION_MIN_WORDS,
            cls.TASK_DESCRIPTION_MAX_WORDS,
        )

    @classmethod
    def display_config(cls) -> None:
        """
        Display current configuration (for debugging).
        Passwords are masked for security.
        """
        print("=" * 50)
        print(f"🚀 {cls.APP_NAME} Configuration")
        print("=" * 50)
        print(f"Environment: {cls.APP_ENV}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"\n📊 Database:")
        print(f"  Host: {cls.DB_HOST}:{cls.DB_PORT}")
        print(f"  Database: {cls.DB_NAME}")
        print(f"  User: {cls.DB_USER}")
        print(f"  Password: {'*' * len(cls.DB_PASSWORD)}")
        print(f"\n⚙️  Limits:")
        print(f"  Max Projects: {cls.MAX_NUMBER_OF_PROJECT}")
        print(f"  Max Tasks: {cls.MAX_NUMBER_OF_TASK}")
        print("=" * 50)
