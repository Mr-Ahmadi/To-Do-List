"""
Dependency injection for FastAPI routes.
Provides database session management for API endpoints.
"""

from typing import Generator
from sqlalchemy.orm import Session
from todolist_app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session to route handlers.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage in routes:
        @router.get("/projects")
        def list_projects(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
