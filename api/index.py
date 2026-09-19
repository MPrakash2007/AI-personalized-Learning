import os
import sys

import re
import traceback

def sanitize_log(text: str) -> str:
    """
    Sanitize sensitive information from logs (passwords, connection strings, JWT, API keys).
    Never leaks credentials to stdout/stderr.
    """
    if not text:
        return ""
    # Redact credentials in database URLs (postgres://, postgresql://, etc.)
    sanitized = re.sub(
        r'(postgres(?:ql)?(?:\+[a-zA-Z0-9_-]+)?://)([^:@/\s]+):([^@/\s]+)@',
        r'\1\2:***@',
        text
    )
    # Redact key-value pairs with sensitive keys
    sanitized = re.sub(
        r'(?i)(password|secret|api[_-]?key|jwt|token)\s*([=:])\s*([^\s,;&"\']+)',
        r'\1\2***',
        sanitized
    )
    return sanitized

# Resolve paths for local, Vercel, and AWS Lambda serverless execution
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
CANDIDATE_PATHS = [
    os.path.join(BASE_DIR, "backend"),
    BASE_DIR,
    CURRENT_DIR,
    os.path.join(os.getcwd(), "backend"),
    os.getcwd(),
    "/var/task/backend",
    "/var/task"
]

for p in CANDIDATE_PATHS:
    if p and os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from starlette.types import ASGIApp, Scope, Receive, Send

fastapi_app = None
startup_error_type = None

try:
    from app.main import app as fastapi_app
except Exception as import_exc:
    startup_error_type = type(import_exc).__name__
    clean_msg = sanitize_log(str(import_exc))
    clean_tb = sanitize_log(traceback.format_exc())

    # Write directly to stderr and flush so Vercel runtime logs capture the exact failure
    sys.stderr.write(f"\n[CRITICAL STARTUP ERROR] {startup_error_type}: {clean_msg}\n")
    sys.stderr.write(f"[STARTUP TRACEBACK]\n{clean_tb}\n\n")
    sys.stderr.flush()

    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    fastapi_app = FastAPI(title="CodeOrbit API Fallback")

    @fastapi_app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
    async def fallback_catchall(path: str):
        return JSONResponse(
            status_code=503,
            content={
                "status": "service_unavailable",
                "service": "CodeOrbit API Fallback",
                "detail": f"Backend initialization failed during startup ({startup_error_type}). Please check server logs for details.",
                "error_type": startup_error_type
            }
        )

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
