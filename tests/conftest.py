# SPDX-License-Identifier: AGPL-3.0-or-later
"""Pytest configuration and fixtures for pdf-agpl-tools tests."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_pdf_base64():
    """A minimal valid PDF encoded as base64."""
    # Minimal valid PDF (empty single page)
    import base64
    minimal_pdf = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj
xref
0 4
0000000000 65535 f
0000000009 00000 n
0000000052 00000 n
0000000101 00000 n
trailer<</Size 4/Root 1 0 R>>
startxref
170
%%EOF"""
    return base64.b64encode(minimal_pdf).decode("utf-8")


@pytest.fixture
def sample_multi_page_pdf_base64():
    """A minimal valid PDF with 3 pages encoded as base64."""
    import base64
    # 3-page PDF
    pdf = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R 4 0 R 5 0 R]/Count 3>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj
4 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj
5 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000052 00000 n
0000000113 00000 n
0000000172 00000 n
0000000231 00000 n
trailer<</Size 6/Root 1 0 R>>
startxref
290
%%EOF"""
    return base64.b64encode(pdf).decode("utf-8")
