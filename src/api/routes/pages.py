# SPDX-License-Identifier: AGPL-3.0-or-later
"""Page operations API routes."""

import base64
import io
import fitz  # PyMuPDF
from fastapi import APIRouter, HTTPException

from src.api.schemas.pages import (
    DeletePagesRequest, DeletePagesResponse,
    InsertBlankRequest, InsertBlankResponse,
    InsertPdfRequest, InsertPdfResponse,
    ExtractPagesRequest, ExtractPagesResponse,
    RotatePagesRequest, RotatePagesResponse,
)
from src.services import page_operations

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


@router.post("/delete", response_model=DeletePagesResponse)
async def delete_pages(request: DeletePagesRequest):
    """Delete specified pages from a PDF."""
    try:
        pdf_bytes = decode_pdf(request.pdf)
        doc = open_pdf_from_bytes(pdf_bytes)

        details = page_operations.delete_pages(
            doc,
            request.pages,
            request.password
        )

        result_bytes = save_pdf_to_bytes(doc)
        doc.close()

        return DeletePagesResponse(
            success=True,
            pdf=encode_pdf(result_bytes),
            details=details
        )
    except ValueError as e:
        return DeletePagesResponse(
            success=False,
            error={"code": "INVALID_INPUT", "message": str(e)}
        )
    except Exception as e:
        return DeletePagesResponse(
            success=False,
            error={"code": "PROCESSING_FAILED", "message": str(e)}
        )


@router.post("/insert-blank", response_model=InsertBlankResponse)
async def insert_blank_page(request: InsertBlankRequest):
    """Insert a blank page before or after a reference page."""
    try:
        pdf_bytes = decode_pdf(request.pdf)
        doc = open_pdf_from_bytes(pdf_bytes)

        details = page_operations.insert_blank_page(
            doc,
            request.position,
            request.reference_page,
            request.width,
            request.height,
            request.password
        )

        result_bytes = save_pdf_to_bytes(doc)
        doc.close()

        return InsertBlankResponse(
            success=True,
            pdf=encode_pdf(result_bytes),
            details=details
        )
    except ValueError as e:
        return InsertBlankResponse(
            success=False,
            error={"code": "INVALID_INPUT", "message": str(e)}
        )
    except Exception as e:
        return InsertBlankResponse(
            success=False,
            error={"code": "PROCESSING_FAILED", "message": str(e)}
        )


@router.post("/insert-pdf", response_model=InsertPdfResponse)
async def insert_pdf_pages(request: InsertPdfRequest):
    """Insert pages from another PDF."""
    try:
        target_bytes = decode_pdf(request.target_pdf)
        source_bytes = decode_pdf(request.source_pdf)

        target_doc = open_pdf_from_bytes(target_bytes)
        source_doc = open_pdf_from_bytes(source_bytes)

        details = page_operations.insert_pdf_pages(
            target_doc,
            source_doc,
            request.position,
            request.reference_page,
            request.pages_to_insert,
            request.target_password,
            request.source_password
        )

        result_bytes = save_pdf_to_bytes(target_doc)
        target_doc.close()
        source_doc.close()

        return InsertPdfResponse(
            success=True,
            pdf=encode_pdf(result_bytes),
            details=details
        )
    except ValueError as e:
        return InsertPdfResponse(
            success=False,
            error={"code": "INVALID_INPUT", "message": str(e)}
        )
    except Exception as e:
        return InsertPdfResponse(
            success=False,
            error={"code": "PROCESSING_FAILED", "message": str(e)}
        )


@router.post("/extract", response_model=ExtractPagesResponse)
async def extract_pages(request: ExtractPagesRequest):
    """Extract (keep) only specified pages from a PDF."""
    try:
        pdf_bytes = decode_pdf(request.pdf)
        doc = open_pdf_from_bytes(pdf_bytes)

        details = page_operations.extract_pages(
            doc,
            request.pages,
            request.password
        )

        result_bytes = save_pdf_to_bytes(doc)
        doc.close()

        return ExtractPagesResponse(
            success=True,
            pdf=encode_pdf(result_bytes),
            details=details
        )
    except ValueError as e:
        return ExtractPagesResponse(
            success=False,
            error={"code": "INVALID_INPUT", "message": str(e)}
        )
    except Exception as e:
        return ExtractPagesResponse(
            success=False,
            error={"code": "PROCESSING_FAILED", "message": str(e)}
        )


@router.post("/rotate", response_model=RotatePagesResponse)
async def rotate_pages(request: RotatePagesRequest):
    """Rotate specified pages by the given angle."""
    try:
        pdf_bytes = decode_pdf(request.pdf)
        doc = open_pdf_from_bytes(pdf_bytes)

        details = page_operations.rotate_pages(
            doc,
            request.pages,
            request.rotation,
            request.password
        )

        result_bytes = save_pdf_to_bytes(doc)
        doc.close()

        return RotatePagesResponse(
            success=True,
            pdf=encode_pdf(result_bytes),
            details=details
        )
    except ValueError as e:
        return RotatePagesResponse(
            success=False,
            error={"code": "INVALID_INPUT", "message": str(e)}
        )
    except Exception as e:
        return RotatePagesResponse(
            success=False,
            error={"code": "PROCESSING_FAILED", "message": str(e)}
        )
