# SPDX-License-Identifier: AGPL-3.0-or-later
"""Main FastAPI application for pdf-agpl-tools."""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.api.routes import health, pages, redaction, compression

app = FastAPI(
    title="pdf-agpl-tools",
    description="PDF manipulation microservice using PyMuPDF and Ghostscript (AGPL-3.0)",
    version=settings.version,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_source_code_header(request: Request, call_next):
    """Add X-Source-Code header to all responses as required by AGPL."""
    response = await call_next(request)
    response.headers["X-Source-Code"] = settings.source_code_url
    return response


@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    """Verify API key for authenticated endpoints."""
    # Skip auth for health check and docs
    if request.url.path in ["/api/v1/health", "/docs", "/openapi.json", "/"]:
        return await call_next(request)

    # Check API key if configured
    if settings.api_key:
        api_key = request.headers.get("X-API-Key")
        if api_key != settings.api_key:
            return JSONResponse(
                status_code=401,
                content={"success": False, "error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}},
            )

    return await call_next(request)


# Register routes
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(pages.router, prefix="/api/v1/pages", tags=["Page Operations"])
app.include_router(redaction.router, prefix="/api/v1", tags=["Redaction"])
app.include_router(compression.router, prefix="/api/v1", tags=["Compression"])


@app.get("/")
async def root():
    """Root endpoint with service info."""
    return {
        "service": settings.service_name,
        "version": settings.version,
        "license": "AGPL-3.0-or-later",
        "source_code": settings.source_code_url,
        "docs": "/docs",
    }
