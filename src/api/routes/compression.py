# SPDX-License-Identifier: AGPL-3.0-or-later
"""Compression API routes."""

import base64
from fastapi import APIRouter

from src.api.schemas.compression import (
    CompressRequest, CompressResponse,
    CompressionMethodsResponse, CompressionMethodInfo
)
from src.services import compression

router = APIRouter()


def decode_pdf(pdf_base64: str) -> bytes:
    """Decode base64 PDF data."""
    try:
        return base64.b64decode(pdf_base64)
    except Exception as e:
        raise ValueError(f"Invalid base64 PDF data: {e}")


def encode_pdf(pdf_bytes: bytes) -> str:
    """Encode PDF bytes to base64."""
    return base64.b64encode(pdf_bytes).decode("utf-8")


@router.post("/compress", response_model=CompressResponse)
async def compress_pdf(request: CompressRequest):
    """Compress a PDF using Ghostscript."""
    try:
        pdf_bytes = decode_pdf(request.pdf)

        result = compression.compress_pdf(
            pdf_bytes,
            request.method,
            request.rasterize or False
        )

        return CompressResponse(
            success=True,
            pdf=encode_pdf(result["data"]),
            stats=result["stats"]
        )
    except ValueError as e:
        return CompressResponse(
            success=False,
            error={"code": "INVALID_INPUT", "message": str(e)}
        )
    except RuntimeError as e:
        return CompressResponse(
            success=False,
            error={"code": "PROCESSING_FAILED", "message": str(e)}
        )
    except Exception as e:
        return CompressResponse(
            success=False,
            error={"code": "PROCESSING_FAILED", "message": str(e)}
        )


@router.get("/compress/methods", response_model=CompressionMethodsResponse)
async def get_compression_methods():
    """Get available compression methods."""
    methods = compression.get_compression_methods()
    return CompressionMethodsResponse(
        methods=[CompressionMethodInfo(**m) for m in methods]
    )
