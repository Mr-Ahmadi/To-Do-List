# todolist_app/main.py
"""
Main entry point for the ToDoList application (Phase 2 - RDB).
Runs either:
- the interactive CLI menu (console mode), or
- the click-based command-line commands.
"""

import sys

from todolist_app.cli import TodoListCLI
from todolist_app.commands import cli as click_cli


def main():
    """
    Entry point that decides:
      - If no arguments -> run interactive menu
      - If arguments exist -> forward to click commands
    """
    try:
        # If user runs: poetry run todolist
        # → start interactive console
        if len(sys.argv) == 1:
            cli = TodoListCLI()
            cli.run()
        else:
            # With args → click commands
            click_cli()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
