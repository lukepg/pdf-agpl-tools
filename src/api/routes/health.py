# SPDX-License-Identifier: AGPL-3.0-or-later
"""Health check endpoints."""

import subprocess
from datetime import datetime
from fastapi import APIRouter

router = APIRouter()


def get_pymupdf_version() -> dict:
    """Check if PyMuPDF is available and get version."""
    try:
        import fitz
        return {"available": True, "version": fitz.version[0]}
    except ImportError:
        return {"available": False, "version": None}


def get_ghostscript_version() -> dict:
    """Check if Ghostscript is available and get version."""
    try:
        result = subprocess.run(
            ["gs", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return {"available": True, "version": result.stdout.strip()}
        return {"available": False, "version": None}
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {"available": False, "version": None}


@router.get("/health")
async def health_check():
    """
    Check service health and dependency availability.

    Returns status of PyMuPDF and Ghostscript dependencies.
    """
    pymupdf = get_pymupdf_version()
    ghostscript = get_ghostscript_version()

    # Determine overall status
    if pymupdf["available"] and ghostscript["available"]:
        status = "healthy"
    elif pymupdf["available"] or ghostscript["available"]:
        status = "degraded"
    else:
        status = "unhealthy"

    return {
        "status": status,
        "services": {
            "pymupdf": pymupdf,
            "ghostscript": ghostscript,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
