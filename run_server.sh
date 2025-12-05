#!/bin/bash
# Script to run the FastAPI development server

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Use API_PORT from environment or default to 8000
PORT=${API_PORT:-8000}

echo "Starting ToDoList API..."
echo "API will be available at: http://localhost:$PORT"
echo "Documentation at: http://localhost:$PORT/docs"
echo ""

poetry run uvicorn todolist_app.api.main:app --reload --host 0.0.0.0 --port $PORT
