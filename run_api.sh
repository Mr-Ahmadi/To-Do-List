#!/bin/bash
# Script to run the FastAPI development server

echo "Starting ToDoList API..."
echo "API will be available at: http://localhost:8000"
echo "Documentation at: http://localhost:8000/docs"
echo ""

poetry run uvicorn todolist_app.api.main:app --reload --host 0.0.0.0 --port 8003
