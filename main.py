from managers.project_manager import ProjectManager
from managers.task_manager import TaskManager
from utils.config import Config
from exceptions import TodoListException


class TodoListCLI:
    """Command Line Interface for ToDoList Application"""
    
    def __init__(self):
        """Initialize the CLI application"""
        self.project_manager = ProjectManager()
        self.current_project = None
        self.running = True
    
    def run(self):
        """Main application loop"""
        print("=" * 60)
        print("Welcome to ToDoList Application".center(60))
        print("=" * 60)
        print()
        
        while self.running:
            self._show_main_menu()
            choice = input("\nEnter your choice: ").strip()
            self._handle_main_menu(choice)
    
    def _show_main_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 60)
        print("MAIN MENU".center(60))
        print("=" * 60)
        
        # Project Management
        print("\n--- Project Management ---")
        print("1. Create Project")
        print("2. List All Projects")
        print("3. Select Project")
        print("4. Update Current Project")
        print("5. Delete Project")
        
        # Task Management (requires selected project)
        print("\n--- Task Management ---")
        if self.current_project:
            print(f"   Current Project: [{self.current_project.name}]")
        else:
            print("   [No project selected - Select a project first]")
        
        print("6. Create Task")
        print("7. List All Tasks")
        print("8. Update Task")
        print("9. Change Task Status")
        print("10. Delete Task")
        
        # System
        print("\n--- System ---")
        print("11. Show Statistics")
        print("0. Exit")
        print("=" * 60)
    
    def _handle_main_menu(self, choice: str):
        """Handle main menu selection"""
        try:
            if choice == '1':
                self._create_project()
            elif choice == '2':
                self._list_projects()
            elif choice == '3':
                self._select_project()
            elif choice == '4':
                self._update_project()
            elif choice == '5':
                self._delete_project()
            elif choice == '6':
                self._create_task()
            elif choice == '7':
                self._list_tasks()
            elif choice == '8':
                self._update_task()
            elif choice == '9':
                self._change_task_status()
            elif choice == '10':
                self._delete_task()
            elif choice == '11':
                self._show_statistics()
            elif choice == '0':
                self._exit_application()
            else:
                print("\n❌ Invalid choice. Please try again.")
        except TodoListException as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
    
    # ======================== Project Management ========================
    
    def _create_project(self):
        """Create a new project"""
        print("\n--- Create New Project ---")
        name = input("Project Name: ").strip()
        description = input("Project Description: ").strip()
        
        project = self.project_manager.create_project(name, description)
        print(f"\n✅ Project created successfully!")
        print(f"   ID: {project.id}")
        print(f"   Name: {project.name}")
        print(f"   Description: {project.description}")
    
    def _list_projects(self):
        """List all projects"""
        print("\n--- All Projects ---")
        projects = self.project_manager.list_projects()
        
        if not projects:
            print("No projects found.")
            return
        
        for project in projects:
            task_count = len(project.tasks)
            print(f"\n[ID: {project.id}] {project.name}")
            print(f"   Description: {project.description}")
            print(f"   Tasks: {task_count}")
            print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    def _select_project(self):
        """Select a project to work with"""
        print("\n--- Select Project ---")
        self._list_projects()
        
        if not self.project_manager.projects:
            return
        
        try:
            project_id = int(input("\nEnter Project ID to select: ").strip())
            project = self.project_manager.get_project(project_id)
            self.current_project = project
            print(f"\n✅ Project '{project.name}' selected successfully!")
        except ValueError:
            print("\n❌ Invalid ID format. Please enter a number.")
    
    def _update_project(self):
        """Update current project"""
        if not self.current_project:
            print("\n❌ No project selected. Please select a project first.")
            return
        
        print(f"\n--- Update Project: {self.current_project.name} ---")
        print("(Leave blank to keep current value)")
        
        name = input(f"New Name [{self.current_project.name}]: ").strip()
        description = input(f"New Description [{self.current_project.description}]: ").strip()
        
        # Only update if values are provided
        name = name if name else None
        description = description if description else None
        
        if not name and not description:
            print("\n❌ No changes made.")
            return
        
        project = self.project_manager.update_project(
            self.current_project.id,
            name=name,
            description=description
        )
        self.current_project = project  # Update reference
        print(f"\n✅ Project updated successfully!")
    
    def _delete_project(self):
        """Delete a project"""
        print("\n--- Delete Project ---")
        self._list_projects()
        
        if not self.project_manager.projects:
            return
        
        try:
            project_id = int(input("\nEnter Project ID to delete: ").strip())
            project = self.project_manager.get_project(project_id)
            
            # Confirmation
            confirm = input(f"\n⚠️  Are you sure you want to delete '{project.name}'? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("\n❌ Deletion cancelled.")
                return
            
            # Clear current project if it's being deleted
            if self.current_project and self.current_project.id == project_id:
                self.current_project = None
            
            self.project_manager.delete_project(project_id)
            print(f"\n✅ Project deleted successfully!")
        except ValueError:
            print("\n❌ Invalid ID format. Please enter a number.")
    
    # ======================== Task Management ========================
    
    def _create_task(self):
        """Create a new task"""
        if not self.current_project:
            print("\n❌ No project selected. Please select a project first.")
            return
        
        print(f"\n--- Create New Task in '{self.current_project.name}' ---")
        title = input("Task Title: ").strip()
        description = input("Task Description: ").strip()
        deadline = input("Deadline (YYYY-MM-DD) [optional]: ").strip()
        
        print(f"\nValid statuses: {', '.join(Config.VALID_STATUSES)}")
        status = input(f"Status (default: {Config.DEFAULT_STATUS}): ").strip()
        if not status:
            status = Config.DEFAULT_STATUS
        
        task_manager = TaskManager(self.current_project)
        task = task_manager.create_task(
            title=title,
            description=description,
            deadline=deadline if deadline else None,
            status=status
        )
        
        print(f"\n✅ Task created successfully!")
        print(f"   ID: {task.id}")
        print(f"   Title: {task.title}")
        print(f"   Status: {task.status}")
        if task.deadline:
            print(f"   Deadline: {task.deadline.strftime('%Y-%m-%d')}")
    
    def _list_tasks(self):
        """List all tasks in current project"""
        if not self.current_project:
            print("\n❌ No project selected. Please select a project first.")
            return
        
        print(f"\n--- Tasks in '{self.current_project.name}' ---")
        print(f"Filter by status? ({', '.join(Config.VALID_STATUSES)}) [Enter to show all]: ", end='')
        status_filter = input().strip()
        
        task_manager = TaskManager(self.current_project)
        tasks = task_manager.list_tasks(status=status_filter if status_filter else None)
        
        if not tasks:
            print("No tasks found.")
            return
        
        for task in tasks:
            deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else "No deadline"
            print(f"\n[ID: {task.id}] {task.title}")
            print(f"   Description: {task.description}")
            print(f"   Status: {task.status}")
            print(f"   Deadline: {deadline_str}")
            print(f"   Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    def _update_task(self):
        """Update a task"""
        if not self.current_project:
            print("\n❌ No project selected. Please select a project first.")
            return
        
        print(f"\n--- Update Task in '{self.current_project.name}' ---")
        self._list_tasks()
        
        if not self.current_project.tasks:
            return
        
        try:
            task_id = int(input("\nEnter Task ID to update: ").strip())
            task_manager = TaskManager(self.current_project)
            task = task_manager.get_task(task_id)
            
            print("\n(Leave blank to keep current value)")
            title = input(f"New Title [{task.title}]: ").strip()
            description = input(f"New Description [{task.description}]: ").strip()
            deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else "None"
            deadline = input(f"New Deadline (YYYY-MM-DD) [{deadline_str}]: ").strip()
            status = input(f"New Status [{task.status}]: ").strip()
            
            # Only update if values are provided
            title = title if title else None
            description = description if description else None
            deadline = deadline if deadline else None
            status = status if status else None
            
            if not any([title, description, deadline, status]):
                print("\n❌ No changes made.")
                return
            
            task_manager.update_task(
                task_id,
                title=title,
                description=description,
                deadline=deadline,
                status=status
            )
            print(f"\n✅ Task updated successfully!")
        except ValueError:
            print("\n❌ Invalid ID format. Please enter a number.")
    
    def _change_task_status(self):
        """Change task status"""
        if not self.current_project:
            print("\n❌ No project selected. Please select a project first.")
            return
        
        print(f"\n--- Change Task Status in '{self.current_project.name}' ---")
        self._list_tasks()
        
        if not self.current_project.tasks:
            return
        
        try:
            task_id = int(input("\nEnter Task ID: ").strip())
            print(f"\nValid statuses: {', '.join(Config.VALID_STATUSES)}")
            new_status = input("New Status: ").strip()
            
            task_manager = TaskManager(self.current_project)
            task_manager.change_task_status(task_id, new_status)
            print(f"\n✅ Task status changed to '{new_status}' successfully!")
        except ValueError:
            print("\n❌ Invalid ID format. Please enter a number.")
    
    def _delete_task(self):
        """Delete a task"""
        if not self.current_project:
            print("\n❌ No project selected. Please select a project first.")
            return
        
        print(f"\n--- Delete Task from '{self.current_project.name}' ---")
        self._list_tasks()
        
        if not self.current_project.tasks:
            return
        
        try:
            task_id = int(input("\nEnter Task ID to delete: ").strip())
            task_manager = TaskManager(self.current_project)
            task = task_manager.get_task(task_id)
            
            # Confirmation
            confirm = input(f"\n⚠️  Are you sure you want to delete '{task.title}'? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("\n❌ Deletion cancelled.")
                return
            
            task_manager.delete_task(task_id)
            print(f"\n✅ Task deleted successfully!")
        except ValueError:
            print("\n❌ Invalid ID format. Please enter a number.")
    
    # ======================== System ========================
    
    def _show_statistics(self):
        """Show application statistics"""
        print("\n" + "=" * 60)
        print("STATISTICS".center(60))
        print("=" * 60)
        
        total_projects = len(self.project_manager.projects)
        total_tasks = self.project_manager.get_total_tasks_count()
        
        print(f"\nProjects: {total_projects} / {Config.MAX_NUMBER_OF_PROJECT}")
        print(f"Total Tasks: {total_tasks}")
        
        if self.current_project:
            task_count = len(self.current_project.tasks)
            print(f"\nCurrent Project: {self.current_project.name}")
            print(f"Tasks in Current Project: {task_count} / {Config.MAX_NUMBER_OF_TASK}")
            
            # Status breakdown
            todo_count = len([t for t in self.current_project.tasks if t.status == 'todo'])
            in_progress_count = len([t for t in self.current_project.tasks if t.status == 'in_progress'])
            done_count = len([t for t in self.current_project.tasks if t.status == 'done'])
            
            print(f"\n  - Todo: {todo_count}")
            print(f"  - In Progress: {in_progress_count}")
            print(f"  - Done: {done_count}")
        
        print("=" * 60)
    
    def _exit_application(self):
        """Exit the application"""
        print("\n" + "=" * 60)
        print("Thank you for using ToDoList Application!".center(60))
        print("=" * 60)
        self.running = False


def main():
    """Application entry point"""
    try:
        app = TodoListCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")


if __name__ == "__main__":
    main()
