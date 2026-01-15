# SPDX-License-Identifier: AGPL-3.0-or-later
"""Pydantic schemas for page operations."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class DeletePagesRequest(BaseModel):
    """Request to delete pages from a PDF."""
    pdf: str = Field(..., description="Base64-encoded PDF data")
    pages: list[int] = Field(..., description="1-indexed page numbers to delete")
    password: Optional[str] = Field(None, description="Password for encrypted PDFs")


class DeletePagesResponse(BaseModel):
    """Response from delete pages operation."""
    success: bool
    pdf: Optional[str] = Field(None, description="Base64-encoded result PDF")
    details: Optional[dict] = None
    error: Optional[dict] = None


class InsertBlankRequest(BaseModel):
    """Request to insert a blank page."""
    pdf: str = Field(..., description="Base64-encoded PDF data")
    position: Literal["before", "after"] = Field("after", description="Insert position relative to reference page")
    reference_page: int = Field(..., description="1-indexed reference page number")
    width: Optional[float] = Field(None, description="Page width (defaults to reference page)")
    height: Optional[float] = Field(None, description="Page height (defaults to reference page)")
    password: Optional[str] = Field(None, description="Password for encrypted PDFs")


class InsertBlankResponse(BaseModel):
    """Response from insert blank page operation."""
    success: bool
    pdf: Optional[str] = Field(None, description="Base64-encoded result PDF")
    details: Optional[dict] = None
    error: Optional[dict] = None


class InsertPdfRequest(BaseModel):
    """Request to insert pages from another PDF."""
    target_pdf: str = Field(..., description="Base64-encoded target PDF data")
    source_pdf: str = Field(..., description="Base64-encoded source PDF data")
    position: Literal["before", "after"] = Field("after", description="Insert position")
    reference_page: int = Field(..., description="1-indexed reference page in target")
    pages_to_insert: Optional[list[int]] = Field(None, description="1-indexed pages from source (defaults to all)")
    target_password: Optional[str] = Field(None, description="Password for target PDF")
    source_password: Optional[str] = Field(None, description="Password for source PDF")


class InsertPdfResponse(BaseModel):
    """Response from insert PDF pages operation."""
    success: bool
    pdf: Optional[str] = Field(None, description="Base64-encoded result PDF")
    details: Optional[dict] = None
    error: Optional[dict] = None


class ExtractPagesRequest(BaseModel):
    """Request to extract pages from a PDF."""
    pdf: str = Field(..., description="Base64-encoded PDF data")
    pages: list[int] = Field(..., description="1-indexed page numbers to extract/keep")
    password: Optional[str] = Field(None, description="Password for encrypted PDFs")


class ExtractPagesResponse(BaseModel):
    """Response from extract pages operation."""
    success: bool
    pdf: Optional[str] = Field(None, description="Base64-encoded result PDF")
    details: Optional[dict] = None
    error: Optional[dict] = None


class RotatePagesRequest(BaseModel):
    """Request to rotate pages in a PDF."""
    pdf: str = Field(..., description="Base64-encoded PDF data")
    pages: list[int] = Field(..., description="1-indexed page numbers to rotate")
    rotation: Literal[90, 180, 270] = Field(..., description="Rotation angle in degrees")
    password: Optional[str] = Field(None, description="Password for encrypted PDFs")


class RotatePagesResponse(BaseModel):
    """Response from rotate pages operation."""
    success: bool
    pdf: Optional[str] = Field(None, description="Base64-encoded result PDF")
    details: Optional[dict] = None
    error: Optional[dict] = None
