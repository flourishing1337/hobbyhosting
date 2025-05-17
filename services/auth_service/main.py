"""Uvicorn entry point."""

from app.main import app as application

# Expose the FastAPI instance for `uvicorn services.auth_service.main:app`
app = application
