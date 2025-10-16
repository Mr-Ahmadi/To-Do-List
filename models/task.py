from datetime import datetime
from typing import Optional


class Task:
    """Task model class"""

    _id_counter = 1

    def __init__(self, title: str, description: str, project_id: int, deadline: Optional[datetime] = None, status: str = "todo"):
        self.id = Task._id_counter
        Task._id_counter += 1

        self.title = title
        self.description = description
        self.project_id = project_id
        self.deadline = deadline
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None, deadline: Optional[datetime] = None, status: Optional[str] = None):
        """Update task details."""
        if title:
            self.title = title
        if description:
            self.description = description
        if deadline:
            self.deadline = deadline
        if status:
            self.status = status
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        deadline_str = self.deadline.strftime("%Y-%m-%d") if self.deadline else "None"
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}', deadline={deadline_str})"
