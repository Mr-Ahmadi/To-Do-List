from datetime import datetime
from typing import List, Optional
from models.task import Task


class Project:
    """Project model class"""

    _id_counter = 1

    def __init__(self, name: str, description: str):
        self.id = Project._id_counter
        Project._id_counter += 1

        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks: List[Task] = []

    def update(self, name: Optional[str] = None, description: Optional[str] = None):
        """Update project details."""
        if name:
            self.name = name
        if description:
            self.description = description
        self.updated_at = datetime.now()

    def add_task(self, task: Task):
        """Add a new task to the project."""
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        """Remove a task by its ID."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """Retrieve all tasks or tasks filtered by status."""
        if status:
            return [task for task in self.tasks if task.status == status]
        return self.tasks

    def __repr__(self) -> str:
        return f"Project(id={self.id}, name='{self.name}', tasks={len(self.tasks)})"