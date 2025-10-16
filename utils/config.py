import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration management class"""
    
    # Maximum limits from environment variables
    MAX_NUMBER_OF_PROJECT = int(os.getenv('MAX_NUMBER_OF_PROJECT', 10))
    MAX_NUMBER_OF_TASK = int(os.getenv('MAX_NUMBER_OF_TASK', 50))
    
    # Word count constraints
    PROJECT_NAME_MAX_WORDS = 30
    PROJECT_DESCRIPTION_MAX_WORDS = 150
    TASK_TITLE_MAX_WORDS = 30
    TASK_DESCRIPTION_MAX_WORDS = 150
    
    # Valid task statuses
    VALID_STATUSES = ['todo', 'in_progress', 'done']
    DEFAULT_STATUS = 'todo'
    
    # Date format
    DATE_FORMAT = '%Y-%m-%d'
