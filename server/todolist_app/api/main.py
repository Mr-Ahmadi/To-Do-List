"""
FastAPI application instance and configuration.
Main entry point for the ToDoList Web API.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import logging

from todolist_app.api.routers import project_router, task_router
from todolist_app.db.session import engine
from todolist_app.db.base import Base
from todolist_app.exceptions.service_exceptions import TodoListException
from todolist_app.utils.config import Config

# Configure logging from Config
logging.basicConfig(
    level=getattr(logging, Config.get_log_level()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager - initializes database on startup."""
    logger.info(f"Starting {Config.get_app_name()} v{Config.get_api_version()}...")
    logger.info(f"Environment: {Config.get_environment()}")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created/verified")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    yield
    logger.info(f"Shutting down {Config.get_app_name()}...")


# Create FastAPI app instance with Config-driven settings
app = FastAPI(
    title=Config.get_app_name(),
    description=f"""
## {Config.get_app_name()} - Management System API

A comprehensive RESTful API for managing projects and tasks.

### Features

* **Projects** - Full CRUD operations for project management
* **Tasks** - Complete task lifecycle management with status tracking
* **Status Workflow** - Track progress (todo → doing → done → archived)
* **Deadline Management** - Set and monitor task deadlines

### Environment

- **Version**: {Config.get_api_version()}
- **Environment**: {Config.get_environment()}
- **Debug Mode**: {Config.is_debug_mode()}

### Quick Start

1. Explore endpoints in the **Swagger UI** below
2. Check `/health` to verify API status
3. Visit `/api/info` for detailed API information

### Documentation

- Interactive docs at `/docs`
- Alternative docs at `/redoc`
- OpenAPI schema at `/openapi.json`

### Validation Limits

- Project name minimum: {Config.PROJECT_NAME_MIN_WORDS} words
- Task description maximum: {Config.TASK_DESCRIPTION_MAX_WORDS} words
    """,
    version=Config.get_api_version(),
    debug=Config.is_debug_mode(),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": f"{Config.get_app_name()} Support",
        "email": "mr-ahmadi2004@outlook.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "Root",
            "description": "Basic API information and navigation"
        },
        {
            "name": "Health",
            "description": "API health monitoring"
        },
        {
            "name": "Projects",
            "description": "Project management operations"
        },
        {
            "name": "Tasks",
            "description": "Task management with status tracking"
        },
        {
            "name": "Info",
            "description": "Detailed API metadata"
        }
    ]
)


def custom_openapi():
    """Custom OpenAPI schema with enhanced metadata."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags
    )
    
    # Use Config to generate server URLs dynamically
    base_url = Config.get_api_base_url()
    openapi_schema["servers"] = [
        {"url": base_url, "description": f"{Config.get_environment()} Server"}
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema



# CORS middleware with Config-driven origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(TodoListException)
async def todolist_exception_handler(request: Request, exc: TodoListException):
    """Handle TodoListException globally with appropriate status codes."""
    status_code = 400
    error_msg = str(exc).lower()
    
    if "not found" in error_msg:
        status_code = 404
    elif "already exists" in error_msg:
        status_code = 409
    
    logger.warning(f"TodoListException: {exc} (Status: {status_code})")
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "status_code": status_code
        }
    )


# Include routers with tags
app.include_router(project_router, prefix="/api", tags=["Projects"])
app.include_router(task_router, prefix="/api", tags=["Tasks"])


@app.get(
    "/",
    tags=["Root"],
    summary="API Welcome",
    description="Root endpoint with API information and documentation links"
)
def root():
    """
    Root endpoint providing API navigation.
    
    Returns basic information about the API including:
    - Version number
    - Documentation links
    - Available endpoints
    """
    return {
        "message": f"Welcome to {Config.get_app_name()}",
        "version": Config.get_api_version(),
        "environment": Config.get_environment(),
        "debug": Config.is_debug_mode(),
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/health",
            "info": "/api/info",
            "projects": "/api/projects",
            "tasks": "/api/tasks"
        }
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Verify API is running and responsive"
)
def health_check():
    """
    Health check endpoint for monitoring.
    
    Used by:
    - Load balancers
    - Container orchestration (Kubernetes, Docker Swarm)
    - Monitoring systems
    """
    return {
        "status": "healthy",
        "service": Config.get_app_name(),
        "version": Config.get_api_version(),
        "environment": Config.get_environment(),
        "debug": Config.is_debug_mode()
    }


@app.get(
    "/api/info",
    tags=["Info"],
    summary="API Information",
    description="Get detailed API capabilities and feature list"
)
def api_info():
    """
    Detailed API information endpoint.
    
    Returns comprehensive metadata about:
    - Available features
    - Endpoint descriptions
    - Status workflow
    - Documentation links
    - Configuration details
    """
    return {
        "api": Config.get_app_name(),
        "version": Config.get_api_version(),
        "environment": Config.get_environment(),
        "debug": Config.is_debug_mode(),
        "server": {
            "host": Config.get_api_host(),
            "port": Config.get_api_port(),
            "base_url": Config.get_api_base_url()
        },
        "features": [
            "Project CRUD operations",
            "Task CRUD operations",
            "Status management (todo/doing/done/archived)",
            "Deadline tracking",
            "Comprehensive error handling",
            "CORS support",
            "Request logging"
        ],
        "endpoints": {
            "projects": "GET/POST/PUT/DELETE /api/projects",
            "tasks": "GET/POST/PUT/DELETE /api/tasks"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "validation": {
            "project_name_min_words": Config.PROJECT_NAME_MIN_WORDS,
            "task_description_max_words": Config.TASK_DESCRIPTION_MAX_WORDS
        },
        "cors": {
            "allowed_origins": Config.get_cors_origins()
        }
    }


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for monitoring and debugging."""
    logger.info(f"➡️  {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"⬅️  Status: {response.status_code}")
    return response


# Main entry point for direct execution
def main():
    """
    Main entry point for running the API directly.
    Useful for development and testing.
    """
    import uvicorn
    
    base_url = Config.get_api_base_url()
    
    logger.info("=" * 70)
    logger.info(f"🚀 Starting {Config.get_app_name()} v{Config.get_api_version()}")
    logger.info(f"📌 Environment: {Config.get_environment()}")
    logger.info(f"🐛 Debug Mode: {Config.is_debug_mode()}")
    logger.info(f"🌐 Server: {base_url}")
    logger.info(f"📚 Docs: {base_url}/docs")
    logger.info(f"📊 ReDoc: {base_url}/redoc")
    logger.info(f"🔍 Log Level: {Config.get_log_level()}")
    logger.info("=" * 70)
    
    uvicorn.run(
        "todolist_app.api.main:app",
        host=Config.get_api_host(),
        port=Config.get_api_port(),
        reload=Config.is_debug_mode(),
        log_level=Config.get_log_level().lower()
    )


if __name__ == "__main__":
    main()
