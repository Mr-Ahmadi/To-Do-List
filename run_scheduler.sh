#!/bin/bash

# ---------------------------------------------
#  ToDoList - AutoClose Scheduler Runner
#  Runs the periodic job for overdue tasks.
#  Works with Poetry + Cron.
# ---------------------------------------------

# Absolute path to your project (CHANGE IF NEEDED)
PROJECT_DIR="/Users/aliahmadi/Documents/Projects/To-Do-List"

# Absolute path to poetry binary
POETRY_BIN="$(which poetry)"

# Log directory
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/scheduler.log"

# Create logs folder if not exist
mkdir -p "$LOG_DIR"

echo "[$(date)] Starting AutoClose Scheduler..." >> "$LOG_FILE"

# Move into project
cd "$PROJECT_DIR" || exit 1

# Run scheduler module
$POETRY_BIN run python -m todolist_app.scheduler.autoclose_runner >> "$LOG_FILE" 2>&1
