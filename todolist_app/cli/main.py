"""
Main CLI module for the ToDoList application.

This module provides the command-line interface for interacting with
the ToDoList application using database persistence.
"""

from typing import Optional

from todolist_app.exceptions.service_exceptions import TodoListException
from todolist_app.services.project_service import ProjectService
from todolist_app.services.task_service import TaskService
from todolist_app.models.project import Project
from todolist_app.models.task import TaskStatus
from todolist_app.utils.config import Config
from todolist_app.db.session import get_db


class TodoListCLI:
    """
    Command-line interface for the ToDoList application.

    This class provides an interactive menu-driven interface for users
    to manage projects and tasks with database persistence.

    Attributes:
        current_project_id (Optional[int]): ID of currently selected project
    """

    def __init__(self):
        """Initialize the CLI."""
        self.current_project_id: Optional[int] = None

    def run(self) -> None:
        """
        Main loop for the CLI application.

        Displays the main menu and handles user input until exit.
        """
        print("=" * 60)
        print("Welcome to ToDoList Application (Database Edition)".center(60))
        print("=" * 60)
        print()

        while True:
            self._display_main_menu()
            choice = input("\nEnter your choice: ").strip()

            try:
                if choice == "1":
                    self._create_project()
                elif choice == "2":
                    self._view_all_projects()
                elif choice == "3":
                    self._select_project()
                elif choice == "4":
                    self._edit_project()
                elif choice == "5":
                    self._delete_project()
                elif choice == "6":
                    self._create_task()
                elif choice == "7":
                    self._view_all_tasks()
                elif choice == "8":
                    self._view_tasks_by_status()
                elif choice == "9":
                    self._edit_task()
                elif choice == "10":
                    self._delete_task()
                elif choice == "11":
                    self._mark_task_as_done()
                elif choice == "12":
                    self._search_projects()
                elif choice == "13":
                    self._search_tasks()
                elif choice == "0":
                    print("\nThank you for using ToDoList Application!")
                    print("Goodbye! 👋")
                    break
                else:
                    print("\n❌ Invalid choice. Please try again.")

            except TodoListException as e:
                print(f"\n❌ Error: {str(e)}")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")

            input("\nPress Enter to continue...")

    def _display_main_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "=" * 60)
        print("MAIN MENU".center(60))
        print("=" * 60)

        # Display current project info
        if self.current_project_id:
            try:
                for db in get_db():
                    service = ProjectService(db)
                    project = service.get_project_by_id(self.current_project_id)
                    task_count = TaskService(db).get_task_count(project.id)
                    print(f"📁 Current Project: {project.name} (ID: {project.id})")
                    print(f"   Tasks: {task_count}")
            except Exception:
                self.current_project_id = None
                print("📁 No project selected")
        else:
            print("📁 No project selected")

        print("-" * 60)
        print("\nProject Management:")
        print("  1. Create Project")
        print("  2. View All Projects")
        print("  3. Select Project")
        print("  4. Edit Project")
        print("  5. Delete Project")

        print("\nTask Management:")
        print("  6. Create Task")
        print("  7. View All Tasks")
        print("  8. View Tasks by Status")
        print("  9. Edit Task")
        print("  10. Delete Task")
        print("  11. Mark Task as Done")

        print("\nSearch:")
        print("  12. Search Projects")
        print("  13. Search Tasks")

        print("\n  0. Exit")
        print("=" * 60)

    def _create_project(self) -> None:
        """Handle project creation."""
        print("\n" + "=" * 60)
        print("CREATE NEW PROJECT".center(60))
        print("=" * 60)

        name = input(
            f"\nProject Name ({Config.PROJECT_NAME_MIN_WORDS}-"
            f"{Config.PROJECT_NAME_MAX_WORDS} words): "
        ).strip()
        description = input(
            f"Description (optional, max {Config.PROJECT_DESCRIPTION_MAX_WORDS} words): "
        ).strip()

        for db in get_db():
            service = ProjectService(db)
            project = service.create_project(
                name, description if description else None
            )
            print(f"\n✅ Project created successfully!")
            print(f"   ID: {project.id}")
            print(f"   Name: {project.name}")

    def _view_all_projects(self) -> None:
        """Display all projects."""
        print("\n" + "=" * 60)
        print("ALL PROJECTS".center(60))
        print("=" * 60)

        for db in get_db():
            service = ProjectService(db)
            projects = service.get_all_projects()

            if not projects:
                print("\n📭 No projects found.")
                return

            for i, project in enumerate(projects, 1):
                task_count = TaskService(db).get_task_count(project.id)
                print(f"\n{i}. Project ID: {project.id}")
                print(f"   Name: {project.name}")
                print(f"   Description: {project.description}")
                print(f"   Tasks: {task_count}")
                print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")

    def _select_project(self) -> None:
        """Handle project selection."""
        print("\n" + "=" * 60)
        print("SELECT PROJECT".center(60))
        print("=" * 60)

        for db in get_db():
            service = ProjectService(db)
            projects = service.get_all_projects()

            if not projects:
                print("\n📭 No projects available. Create a project first.")
                return

            # Display projects
            for i, project in enumerate(projects, 1):
                task_count = TaskService(db).get_task_count(project.id)
                print(f"{i}. {project.name} (ID: {project.id}) - {task_count} tasks")

            choice = input("\nEnter project number or ID: ").strip()

            try:
                # Try as index first
                if choice.isdigit() and 1 <= int(choice) <= len(projects):
                    selected_project = projects[int(choice) - 1]
                    self.current_project_id = selected_project.id
                else:
                    # Try as ID
                    project_id = int(choice)
                    project = service.get_project_by_id(project_id)
                    self.current_project_id = project.id

                print(f"\n✅ Project selected!")
            except (ValueError, TodoListException):
                print("\n❌ Invalid selection.")

    def _edit_project(self) -> None:
        """Handle project editing."""
        print("\n" + "=" * 60)
        print("EDIT PROJECT".center(60))
        print("=" * 60)

        for db in get_db():
            service = ProjectService(db)
            projects = service.get_all_projects()

            if not projects:
                print("\n📭 No projects available.")
                return

            # Display projects
            for i, project in enumerate(projects, 1):
                print(f"{i}. {project.name} (ID: {project.id})")

            choice = input("\nEnter project number or ID to edit: ").strip()

            try:
                # Get project
                if choice.isdigit() and 1 <= int(choice) <= len(projects):
                    project = projects[int(choice) - 1]
                else:
                    project_id = int(choice)
                    project = service.get_project_by_id(project_id)

                print(f"\nCurrent Name: {project.name}")
                print(f"Current Description: {project.description}")

                name = input("\nNew Name (or press Enter to keep current): ").strip()
                description = input(
                    f"New Description (optional, max "
                    f"{Config.PROJECT_DESCRIPTION_MAX_WORDS} words, "
                    f"or press Enter to keep current): "
                ).strip()

                # Update project
                service.update_project(
                    project.id,
                    name=name if name else None,
                    description=description if description else None,
                )

                print("\n✅ Project updated successfully!")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    def _delete_project(self) -> None:
        """Handle project deletion."""
        print("\n" + "=" * 60)
        print("DELETE PROJECT".center(60))
        print("=" * 60)

        for db in get_db():
            proj_service = ProjectService(db)
            task_service = TaskService(db)
            projects = proj_service.get_all_projects()

            if not projects:
                print("\n📭 No projects available.")
                return

            # Display projects
            for i, project in enumerate(projects, 1):
                task_count = task_service.get_task_count(project.id)
                print(f"{i}. {project.name} (ID: {project.id}) - {task_count} tasks")

            choice = input("\nEnter project number or ID to delete: ").strip()

            try:
                # Get project
                if choice.isdigit() and 1 <= int(choice) <= len(projects):
                    project = projects[int(choice) - 1]
                else:
                    project_id = int(choice)
                    project = proj_service.get_project_by_id(project_id)

                task_count = task_service.get_task_count(project.id)

                # Confirm deletion
                print(f"\n⚠️  WARNING: This will delete the project '{project.name}'")
                print(f"   and all its {task_count} tasks permanently!")
                confirm = input("\nType 'DELETE' to confirm: ").strip()

                if confirm == "DELETE":
                    proj_service.delete_project(project.id)

                    # Clear current project if deleted
                    if self.current_project_id == project.id:
                        self.current_project_id = None

                    print("\n✅ Project deleted successfully!")
                else:
                    print("\n❌ Deletion cancelled.")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    def _create_task(self) -> None:
        """Handle task creation."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("CREATE NEW TASK".center(60))
        print("=" * 60)

        for db in get_db():
            proj_service = ProjectService(db)
            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.name}\n")

            title = input(
                f"Task Title ({Config.TASK_TITLE_MIN_WORDS}-"
                f"{Config.TASK_TITLE_MAX_WORDS} words): "
            ).strip()
            description = input(
                f"Description ({Config.TASK_DESCRIPTION_MIN_WORDS}-"
                f"{Config.TASK_DESCRIPTION_MAX_WORDS} words): "
            ).strip()
            deadline = input("Deadline (YYYY-MM-DD) or leave blank: ").strip()

            print(f"\nValid statuses: {', '.join(Config.get_valid_statuses())}")
            status = input("Status (default: todo): ").strip() or "todo"

            task_service = TaskService(db)
            task = task_service.create_task(
                project_id=self.current_project_id,
                title=title,
                description=description,
                deadline=deadline if deadline else None,
                status=status,
            )

            print(f"\n✅ Task created successfully!")
            print(f"   ID: {task.id}")
            print(f"   Title: {task.title}")
            print(f"   Status: {task.status.value}")

    def _view_all_tasks(self) -> None:
        """Display all tasks in the current project."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("ALL TASKS".center(60))
        print("=" * 60)

        for db in get_db():
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.name}\n")

            tasks = task_service.get_tasks_by_project(self.current_project_id)

            if not tasks:
                print("📭 No tasks found in this project.")
                return

            for i, task in enumerate(tasks, 1):
                deadline_str = (
                    task.deadline.strftime("%Y-%m-%d")
                    if task.deadline
                    else "No deadline"
                )
                print(f"\n{i}. Task ID: {task.id}")
                print(f"   Title: {task.title}")
                print(f"   Description: {task.description}")
                print(f"   Status: {task.status.value}")
                print(f"   Deadline: {deadline_str}")

    def _view_tasks_by_status(self) -> None:
        """Display tasks filtered by status."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("VIEW TASKS BY STATUS".center(60))
        print("=" * 60)

        for db in get_db():
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.name}\n")

            print(f"Valid statuses: {', '.join(Config.get_valid_statuses())}")
            status = input("\nEnter status: ").strip().lower()

            tasks = task_service.get_tasks_by_status(self.current_project_id, status)

            if not tasks:
                print(f"\n📭 No tasks with status '{status}' found.")
                return

            print(f"\nTasks with status '{status}':")
            for i, task in enumerate(tasks, 1):
                deadline_str = (
                    task.deadline.strftime("%Y-%m-%d")
                    if task.deadline
                    else "No deadline"
                )
                print(f"\n{i}. Task ID: {task.id}")
                print(f"   Title: {task.title}")
                print(f"   Deadline: {deadline_str}")

    def _edit_task(self) -> None:
        """Handle task editing."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("EDIT TASK".center(60))
        print("=" * 60)

        for db in get_db():
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.name}\n")

            tasks = task_service.get_tasks_by_project(self.current_project_id)

            if not tasks:
                print("📭 No tasks available.")
                return

            # Display tasks
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title} (ID: {task.id}) - Status: {task.status.value}")

            choice = input("\nEnter task number or ID to edit: ").strip()

            try:
                # Get task
                if choice.isdigit() and 1 <= int(choice) <= len(tasks):
                    task = tasks[int(choice) - 1]
                else:
                    task_id = int(choice)
                    task = task_service.get_task_by_id(task_id)

                print(f"\nCurrent Title: {task.title}")
                print(f"Current Description: {task.description}")
                print(f"Current Status: {task.status.value}")
                print(
                    f"Current Deadline: "
                    f"{task.deadline.strftime('%Y-%m-%d') if task.deadline else 'None'}"
                )

                title = input("\nNew Title (or press Enter to keep current): ").strip()
                description = input(
                    "New Description (or press Enter to keep current): "
                ).strip()
                deadline = input(
                    "New Deadline (YYYY-MM-DD) or press Enter to keep current: "
                ).strip()

                print(f"\nValid statuses: {', '.join(Config.get_valid_statuses())}")
                status = input("New Status (or press Enter to keep current): ").strip()

                # Update task
                task_service.update_task(
                    task.id,
                    title=title if title else None,
                    description=description if description else None,
                    deadline=deadline if deadline else None,
                    status=status if status else None,
                )

                print("\n✅ Task updated successfully!")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    def _delete_task(self) -> None:
        """Handle task deletion."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("DELETE TASK".center(60))
        print("=" * 60)

        for db in get_db():
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.name}\n")

            tasks = task_service.get_tasks_by_project(self.current_project_id)

            if not tasks:
                print("📭 No tasks available.")
                return

            # Display tasks
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title} (ID: {task.id})")

            choice = input("\nEnter task number or ID to delete: ").strip()

            try:
                # Get task
                if choice.isdigit() and 1 <= int(choice) <= len(tasks):
                    task = tasks[int(choice) - 1]
                else:
                    task_id = int(choice)
                    task = task_service.get_task_by_id(task_id)

                # Confirm deletion
                confirm = input(
                    f"\nAre you sure you want to delete '{task.title}'? (yes/no): "
                ).strip().lower()

                if confirm == "yes":
                    task_service.delete_task(task.id)
                    print("\n✅ Task deleted successfully!")
                else:
                    print("\n❌ Deletion cancelled.")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    def _mark_task_as_done(self) -> None:
        """Handle marking a task as done."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("MARK TASK AS DONE".center(60))
        print("=" * 60)

        for db in get_db():
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.name}\n")

            # Get all tasks and filter pending ones
            all_tasks = task_service.get_tasks_by_project(self.current_project_id)
            pending_tasks = [t for t in all_tasks if t.status != TaskStatus.DONE]

            if not pending_tasks:
                print("📭 No pending tasks to complete.")
                return

            # Display pending tasks
            for i, task in enumerate(pending_tasks, 1):
                print(f"{i}. {task.title} (ID: {task.id}) - Status: {task.status.value}")

            choice = input("\nEnter task number or ID to mark as done: ").strip()

            try:
                # Get task
                if choice.isdigit() and 1 <= int(choice) <= len(pending_tasks):
                    task = pending_tasks[int(choice) - 1]
                else:
                    task_id = int(choice)
                    task = task_service.get_task_by_id(task_id)

                task_service.mark_task_as_done(task.id)
                print(f"\n✅ Task '{task.title}' marked as done!")

            except (ValueError, TodoListException) as e:
                print(f"\n❌ Error: {str(e)}")

    def _search_projects(self) -> None:
        """Search projects by name or description."""
        print("\n" + "=" * 60)
        print("SEARCH PROJECTS".center(60))
        print("=" * 60)

        query = input("\nEnter search term: ").strip()

        if not query:
            print("\n❌ Search term cannot be empty.")
            return

        for db in get_db():
            service = ProjectService(db)
            projects = service.search_projects(query)

            if not projects:
                print(f"\n📭 No projects found matching '{query}'.")
                return

            print(f"\nFound {len(projects)} project(s):")
            for i, project in enumerate(projects, 1):
                task_count = TaskService(db).get_task_count(project.id)
                print(f"\n{i}. Project ID: {project.id}")
                print(f"   Name: {project.name}")
                print(f"   Description: {project.description}")
                print(f"   Tasks: {task_count}")

    def _search_tasks(self) -> None:
        """Search tasks in current project."""
        if not self.current_project_id:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("SEARCH TASKS".center(60))
        print("=" * 60)

        for db in get_db():
            proj_service = ProjectService(db)
            task_service = TaskService(db)

            project = proj_service.get_project_by_id(self.current_project_id)
            print(f"Project: {project.name}\n")

            query = input("Enter search term: ").strip()

            if not query:
                print("\n❌ Search term cannot be empty.")
                return

            tasks = task_service.search_tasks(self.current_project_id, query)

            if not tasks:
                print(f"\n📭 No tasks found matching '{query}'.")
                return

            print(f"\nFound {len(tasks)} task(s):")
            for i, task in enumerate(tasks, 1):
                print(f"\n{i}. Task ID: {task.id}")
                print(f"   Title: {task.title}")
                print(f"   Status: {task.status.value}")


def main():
    """
    Main entry point for the ToDoList application.

    This function initializes and runs the CLI interface.
    """
    try:
        cli = TodoListCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
