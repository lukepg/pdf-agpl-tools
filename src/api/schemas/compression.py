# SPDX-License-Identifier: AGPL-3.0-or-later
"""Pydantic schemas for compression operations."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


CompressionMethod = Literal["gs-minimum", "gs-screen", "gs-ebook", "gs-printer"]


class CompressRequest(BaseModel):
    """Request to compress a PDF."""
    pdf: str = Field(..., description="Base64-encoded PDF data")
    method: CompressionMethod = Field(..., description="Compression method/quality preset")
    rasterize: Optional[bool] = Field(False, description="Flatten pages to images")


class CompressResponse(BaseModel):
    """Response from compression operation."""
    success: bool
    pdf: Optional[str] = Field(None, description="Base64-encoded result PDF")
    stats: Optional[dict] = Field(None, description="Compression statistics")
    error: Optional[dict] = None


class CompressionMethodInfo(BaseModel):
    """Information about a compression method."""
    method: str
    name: str
    description: str
    dpi: int


class CompressionMethodsResponse(BaseModel):
    """Response listing available compression methods."""
    methods: list[CompressionMethodInfo]
