"""
Database session management module.

This module handles database connections and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://todouser:todopass@localhost:5432/todolist_db"
)

# Create SQLAlchemy engine
# echo=True will print all SQL statements (useful for debugging)
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True  # Verify connections before using them
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


def get_db():
    """
    Dependency function to get database session.
    
    This function creates a new database session for each request
    and ensures it's properly closed after use.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        >>> for db in get_db():
        >>>     # Use db session here
        >>>     pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
