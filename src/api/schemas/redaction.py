# SPDX-License-Identifier: AGPL-3.0-or-later
"""Pydantic schemas for redaction operations."""

from typing import Optional, Union
from pydantic import BaseModel, Field


class RedactionArea(BaseModel):
    """A single redaction area."""
    page: int = Field(..., description="1-indexed page number")
    x: float = Field(..., description="X coordinate of redaction area")
    y: float = Field(..., description="Y coordinate of redaction area")
    width: float = Field(..., description="Width of redaction area")
    height: float = Field(..., description="Height of redaction area")
    fill: Optional[Union[str, list[float]]] = Field(
        "#FFFFFF",
        description="Fill color (hex string or RGB list 0-1)"
    )


class ReplacementText(BaseModel):
    """Replacement text to add after redaction."""
    page: int = Field(..., description="1-indexed page number")
    x: float = Field(..., description="X coordinate for text")
    y: float = Field(..., description="Y coordinate for text")
    text: str = Field(..., description="Text to insert")
    fontsize: Optional[float] = Field(12, description="Font size")
    color: Optional[Union[str, list[float]]] = Field(
        "#000000",
        description="Text color (hex string or RGB list 0-1)"
    )


class RedactRequest(BaseModel):
    """Request to apply redactions to a PDF."""
    pdf: str = Field(..., description="Base64-encoded PDF data")
    redactions: list[RedactionArea] = Field(..., description="List of redaction areas")
    replacement_texts: Optional[list[ReplacementText]] = Field(
        None,
        description="Optional replacement texts to add after redaction"
    )
    password: Optional[str] = Field(None, description="Password for encrypted PDFs")


class RedactResponse(BaseModel):
    """Response from redaction operation."""
    success: bool
    pdf: Optional[str] = Field(None, description="Base64-encoded result PDF")
    error: Optional[dict] = None
