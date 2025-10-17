"""
Main CLI module for the ToDoList application.

This module provides the command-line interface for interacting with
the ToDoList application.
"""

from typing import Optional

from todolist_app.exceptions.custom_exceptions import TodoListException
from todolist_app.managers.project_manager import ProjectManager
from todolist_app.managers.task_manager import TaskManager
from todolist_app.models.project import Project
from todolist_app.utils.config import Config


class TodoListCLI:
    """
    Command-line interface for the ToDoList application.

    This class provides an interactive menu-driven interface for users
    to manage projects and tasks.

    Attributes:
        project_manager (ProjectManager): Manager for project operations
        current_project (Optional[Project]): Currently selected project
    """

    def __init__(self):
        """Initialize the CLI with a project manager."""
        self.project_manager = ProjectManager()
        self.current_project: Optional[Project] = None

    def run(self) -> None:
        """
        Main loop for the CLI application.

        Displays the main menu and handles user input until exit.
        """
        print("=" * 60)
        print("Welcome to ToDoList Application".center(60))
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
        if self.current_project:
            print(f"📁 Current Project: {self.current_project.name}")
            print(f"   Tasks: {len(self.current_project.tasks)}")
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

        print("\n  0. Exit")
        print("=" * 60)

    def _create_project(self) -> None:
        """Handle project creation."""
        print("\n" + "=" * 60)
        print("CREATE NEW PROJECT".center(60))
        print("=" * 60)

        name = input(f"\nProject Name ({Config.PROJECT_NAME_MIN_WORDS}-{Config.PROJECT_NAME_MAX_WORDS} words): ").strip()
        description = input(f"Description ({Config.PROJECT_DESCRIPTION_MIN_WORDS}-{Config.PROJECT_DESCRIPTION_MAX_WORDS} words): ").strip()

        project = self.project_manager.create_project(name, description)
        print(f"\n✅ Project created successfully!")
        print(f"   ID: {project.id}")
        print(f"   Name: {project.name}")

    def _view_all_projects(self) -> None:
        """Display all projects."""
        print("\n" + "=" * 60)
        print("ALL PROJECTS".center(60))
        print("=" * 60)

        projects = self.project_manager.get_all_projects()

        if not projects:
            print("\n📭 No projects found.")
            return

        for i, project in enumerate(projects, 1):
            print(f"\n{i}. Project ID: {project.id}")
            print(f"   Name: {project.name}")
            print(f"   Description: {project.description}")
            print(f"   Tasks: {len(project.tasks)}")
            print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")

    def _select_project(self) -> None:
        """Handle project selection."""
        print("\n" + "=" * 60)
        print("SELECT PROJECT".center(60))
        print("=" * 60)

        projects = self.project_manager.get_all_projects()

        if not projects:
            print("\n📭 No projects available. Create a project first.")
            return

        # Display projects
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project.name} (ID: {project.id}) - {len(project.tasks)} tasks")

        choice = input("\nEnter project number or ID: ").strip()

        try:
            # Try as index first
            if choice.isdigit() and 1 <= int(choice) <= len(projects):
                self.current_project = projects[int(choice) - 1]
            else:
                # Try as ID
                project_id = int(choice)
                self.current_project = self.project_manager.get_project_by_id(
                    project_id
                )

            print(f"\n✅ Project '{self.current_project.name}' selected!")
        except (ValueError, TodoListException):
            print("\n❌ Invalid selection.")

    def _edit_project(self) -> None:
        """Handle project editing."""
        print("\n" + "=" * 60)
        print("EDIT PROJECT".center(60))
        print("=" * 60)

        projects = self.project_manager.get_all_projects()

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
                project = self.project_manager.get_project_by_id(project_id)

            print(f"\nCurrent Name: {project.name}")
            print(f"Current Description: {project.description}")

            name = input("\nNew Name (or press Enter to keep current): ").strip()
            description = input("New Description (or press Enter to keep current): ").strip()

            # Update project
            self.project_manager.update_project(
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

        projects = self.project_manager.get_all_projects()

        if not projects:
            print("\n📭 No projects available.")
            return

        # Display projects
        for i, project in enumerate(projects, 1):
            print(
                f"{i}. {project.name} (ID: {project.id}) - {len(project.tasks)} tasks"
            )

        choice = input("\nEnter project number or ID to delete: ").strip()

        try:
            # Get project
            if choice.isdigit() and 1 <= int(choice) <= len(projects):
                project = projects[int(choice) - 1]
            else:
                project_id = int(choice)
                project = self.project_manager.get_project_by_id(project_id)

            # Confirm deletion
            print(f"\n⚠️  WARNING: This will delete the project '{project.name}'")
            print(f"   and all its {len(project.tasks)} tasks permanently!")
            confirm = input("\nType 'DELETE' to confirm: ").strip()

            if confirm == "DELETE":
                self.project_manager.delete_project(project.id)

                # Clear current project if deleted
                if self.current_project and self.current_project.id == project.id:
                    self.current_project = None

                print("\n✅ Project deleted successfully!")
            else:
                print("\n❌ Deletion cancelled.")

        except (ValueError, TodoListException) as e:
            print(f"\n❌ Error: {str(e)}")

    def _create_task(self) -> None:
        """Handle task creation."""
        if not self.current_project:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("CREATE NEW TASK".center(60))
        print("=" * 60)
        print(f"Project: {self.current_project.name}\n")

        title = input(f"Task Title ({Config.TASK_TITLE_MIN_WORDS}-{Config.TASK_TITLE_MAX_WORDS} words): ").strip()
        description = input(f"Description ({Config.TASK_DESCRIPTION_MIN_WORDS}-{Config.TASK_DESCRIPTION_MAX_WORDS} words): ").strip()
        deadline = input("Deadline (YYYY-MM-DD) or leave blank: ").strip()

        print(f"\nValid statuses: {', '.join(Config.get_valid_statuses())}")
        status = input("Status (default: todo): ").strip() or "todo"

        task_manager = TaskManager(self.current_project)
        task = task_manager.create_task(
            title=title, description=description, deadline=deadline, status=status
        )

        print(f"\n✅ Task created successfully!")
        print(f"   ID: {task.id}")
        print(f"   Title: {task.title}")
        print(f"   Status: {task.status}")

    def _view_all_tasks(self) -> None:
        """Display all tasks in the current project."""
        if not self.current_project:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("ALL TASKS".center(60))
        print("=" * 60)
        print(f"Project: {self.current_project.name}\n")

        if not self.current_project.tasks:
            print("📭 No tasks found in this project.")
            return

        for i, task in enumerate(self.current_project.tasks, 1):
            deadline_str = (
                task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
            )
            print(f"\n{i}. Task ID: {task.id}")
            print(f"   Title: {task.title}")
            print(f"   Description: {task.description}")
            print(f"   Status: {task.status}")
            print(f"   Deadline: {deadline_str}")

    def _view_tasks_by_status(self) -> None:
        """Display tasks filtered by status."""
        if not self.current_project:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("VIEW TASKS BY STATUS".center(60))
        print("=" * 60)
        print(f"Project: {self.current_project.name}\n")

        print(f"Valid statuses: {', '.join(Config.get_valid_statuses())}")
        status = input("\nEnter status: ").strip().lower()

        task_manager = TaskManager(self.current_project)
        tasks = task_manager.get_tasks_by_status(status)

        if not tasks:
            print(f"\n📭 No tasks with status '{status}' found.")
            return

        print(f"\nTasks with status '{status}':")
        for i, task in enumerate(tasks, 1):
            deadline_str = (
                task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
            )
            print(f"\n{i}. Task ID: {task.id}")
            print(f"   Title: {task.title}")
            print(f"   Deadline: {deadline_str}")

    def _edit_task(self) -> None:
        """Handle task editing."""
        if not self.current_project:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("EDIT TASK".center(60))
        print("=" * 60)
        print(f"Project: {self.current_project.name}\n")

        if not self.current_project.tasks:
            print("📭 No tasks available.")
            return

        # Display tasks
        for i, task in enumerate(self.current_project.tasks, 1):
            print(f"{i}. {task.title} (ID: {task.id}) - Status: {task.status}")

        choice = input("\nEnter task number or ID to edit: ").strip()

        try:
            task_manager = TaskManager(self.current_project)

            # Get task
            if choice.isdigit() and 1 <= int(choice) <= len(self.current_project.tasks):
                task = self.current_project.tasks[int(choice) - 1]
            else:
                task_id = int(choice)
                task = task_manager.get_task_by_id(task_id)

            print(f"\nCurrent Title: {task.title}")
            print(f"Current Description: {task.description}")
            print(f"Current Status: {task.status}")
            print(f"Current Deadline: {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'None'}")

            title = input("\nNew Title (or press Enter to keep current): ").strip()
            description = input("New Description (or press Enter to keep current): ").strip()
            deadline = input("New Deadline (YYYY-MM-DD) or press Enter to keep current: ").strip()
            
            print(f"\nValid statuses: {', '.join(Config.get_valid_statuses())}")
            status = input("New Status (or press Enter to keep current): ").strip()

            # Update task
            task_manager.update_task(
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
        if not self.current_project:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("DELETE TASK".center(60))
        print("=" * 60)
        print(f"Project: {self.current_project.name}\n")

        if not self.current_project.tasks:
            print("📭 No tasks available.")
            return

        # Display tasks
        for i, task in enumerate(self.current_project.tasks, 1):
            print(f"{i}. {task.title} (ID: {task.id})")

        choice = input("\nEnter task number or ID to delete: ").strip()

        try:
            task_manager = TaskManager(self.current_project)

            # Get task
            if choice.isdigit() and 1 <= int(choice) <= len(self.current_project.tasks):
                task = self.current_project.tasks[int(choice) - 1]
            else:
                task_id = int(choice)
                task = task_manager.get_task_by_id(task_id)

            # Confirm deletion
            confirm = input(f"\nAre you sure you want to delete '{task.title}'? (yes/no): ").strip().lower()

            if confirm == "yes":
                task_manager.delete_task(task.id)
                print("\n✅ Task deleted successfully!")
            else:
                print("\n❌ Deletion cancelled.")

        except (ValueError, TodoListException) as e:
            print(f"\n❌ Error: {str(e)}")

    def _mark_task_as_done(self) -> None:
        """Handle marking a task as done."""
        if not self.current_project:
            print("\n❌ Please select a project first.")
            return

        print("\n" + "=" * 60)
        print("MARK TASK AS DONE".center(60))
        print("=" * 60)
        print(f"Project: {self.current_project.name}\n")

        # Show only pending tasks
        pending_tasks = [
            task for task in self.current_project.tasks if task.status != "done"
        ]

        if not pending_tasks:
            print("📭 No pending tasks to complete.")
            return

        # Display pending tasks
        for i, task in enumerate(pending_tasks, 1):
            print(f"{i}. {task.title} (ID: {task.id}) - Status: {task.status}")

        choice = input("\nEnter task number or ID to mark as done: ").strip()

        try:
            task_manager = TaskManager(self.current_project)

            # Get task
            if choice.isdigit() and 1 <= int(choice) <= len(pending_tasks):
                task = pending_tasks[int(choice) - 1]
            else:
                task_id = int(choice)
                task = task_manager.get_task_by_id(task_id)

            task_manager.mark_task_as_done(task.id)
            print(f"\n✅ Task '{task.title}' marked as done!")

        except (ValueError, TodoListException) as e:
            print(f"\n❌ Error: {str(e)}")


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
