# SPDX-License-Identifier: AGPL-3.0-or-later
"""Redaction API routes."""

import base64
import fitz  # PyMuPDF
from fastapi import APIRouter

from src.api.schemas.redaction import RedactRequest, RedactResponse
from src.services import redaction

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


def open_pdf_from_bytes(pdf_bytes: bytes) -> fitz.Document:
    """Open a PyMuPDF document from bytes."""
    try:
        return fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Invalid PDF file: {e}")


def save_pdf_to_bytes(doc: fitz.Document) -> bytes:
    """Save a PyMuPDF document to bytes."""
    return doc.tobytes(garbage=4, deflate=True)


@router.post("/redact", response_model=RedactResponse)
async def apply_redactions(request: RedactRequest):
    """Apply true redactions to a PDF (removes content from streams)."""
    try:
        pdf_bytes = decode_pdf(request.pdf)
        doc = open_pdf_from_bytes(pdf_bytes)

        # Convert Pydantic models to dicts
        redactions_list = [r.model_dump() for r in request.redactions]
        replacement_texts_list = (
            [t.model_dump() for t in request.replacement_texts]
            if request.replacement_texts
            else None
        )

        redaction.apply_redactions(
            doc,
            redactions_list,
            replacement_texts_list,
            request.password
        )

        result_bytes = save_pdf_to_bytes(doc)
        doc.close()

        return RedactResponse(
            success=True,
            pdf=encode_pdf(result_bytes)
        )
    except ValueError as e:
        return RedactResponse(
            success=False,
            error={"code": "INVALID_INPUT", "message": str(e)}
        )
    except Exception as e:
        return RedactResponse(
            success=False,
            error={"code": "PROCESSING_FAILED", "message": str(e)}
        )
