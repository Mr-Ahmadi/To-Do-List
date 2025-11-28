"""
Database session management module.

This module handles database connections and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from todolist_app.utils.config import Config

# Get database URL from Config
DATABASE_URL = Config.get_database_url(sync=True)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging SQL queries
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Number of connections to maintain
    max_overflow=10  # Max connections beyond pool_size
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """
    Get a database session.
    
    Returns:
        Session: SQLAlchemy database session
        
    Example:
        >>> db = get_db()
        >>> try:
        >>>     # Use db session
        >>>     pass
        >>> finally:
        >>>     db.close()
    """
    return SessionLocal()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions.
    
    Automatically commits on success and rolls back on error.
    Always closes the session when done.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        >>> with get_db_context() as db:
        >>>     # Use db session here
        >>>     # Automatically commits if no exception
        >>>     pass
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
