import os
import sys

# Add the backend directory to Python sys.path so app and curriculum can be imported cleanly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app as fastapi_app
from starlette.types import ASGIApp, Scope, Receive, Send

class VercelPathNormalizationMiddleware:
    """
    Ensures that incoming requests to Vercel Serverless Python functions
    always map correctly to FastAPI routes.

    FastAPI mounts routers under settings.API_V1_STR (default '/api').
    If Vercel forwards the request with or without the '/api' prefix,
    this middleware normalizes the path so that routes match consistently
    without 404 errors.
    """
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "websocket"):
            path = scope.get("path", "")
            # If path does not start with /api and is not root health check (/ or empty)
            if not path.startswith("/api") and path not in ("/", ""):
                scope = dict(scope)
                scope["path"] = f"/api{path}"
        await self.app(scope, receive, send)

# Export app for Vercel Serverless Function runtime
app = VercelPathNormalizationMiddleware(fastapi_app)
