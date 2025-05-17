"""Auth service entry point.

This module simply re-exports the FastAPI ``app`` instance defined in
``auth_service.app.main`` so that tools like ``uvicorn`` can run it directly.
"""

from auth_service.app.main import app

