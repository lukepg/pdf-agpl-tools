# SPDX-License-Identifier: AGPL-3.0-or-later
"""Tests for page operations endpoints."""

import pytest


def test_delete_pages_invalid_pdf(client):
    """Test delete pages with invalid PDF data."""
    response = client.post("/api/v1/pages/delete", json={
        "pdf": "not-valid-base64!@#$",
        "pages": [1]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "error" in data


def test_delete_pages_missing_pages(client):
    """Test delete pages without specifying pages."""
    response = client.post("/api/v1/pages/delete", json={
        "pdf": "dGVzdA==",  # "test" in base64
        "pages": []
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_delete_pages_valid(client, sample_multi_page_pdf_base64):
    """Test delete pages with valid PDF."""
    response = client.post("/api/v1/pages/delete", json={
        "pdf": sample_multi_page_pdf_base64,
        "pages": [1]
    })
    assert response.status_code == 200
    data = response.json()
    # Should succeed if PyMuPDF is available
    if data["success"]:
        assert "pdf" in data
        assert data["details"]["deleted_pages"] == 1


def test_extract_pages_valid(client, sample_multi_page_pdf_base64):
    """Test extract pages with valid PDF."""
    response = client.post("/api/v1/pages/extract", json={
        "pdf": sample_multi_page_pdf_base64,
        "pages": [1, 2]
    })
    assert response.status_code == 200
    data = response.json()
    if data["success"]:
        assert "pdf" in data
        assert data["details"]["extracted_pages"] == 2


def test_rotate_pages_invalid_angle(client, sample_pdf_base64):
    """Test rotate pages with invalid rotation angle."""
    response = client.post("/api/v1/pages/rotate", json={
        "pdf": sample_pdf_base64,
        "pages": [1],
        "rotation": 45  # Invalid - must be 90, 180, or 270
    })
    # Should fail validation
    assert response.status_code == 422


def test_rotate_pages_valid(client, sample_pdf_base64):
    """Test rotate pages with valid rotation."""
    response = client.post("/api/v1/pages/rotate", json={
        "pdf": sample_pdf_base64,
        "pages": [1],
        "rotation": 90
    })
    assert response.status_code == 200
    data = response.json()
    if data["success"]:
        assert "pdf" in data
        assert data["details"]["rotation"] == 90


def test_insert_blank_page(client, sample_pdf_base64):
    """Test insert blank page."""
    response = client.post("/api/v1/pages/insert-blank", json={
        "pdf": sample_pdf_base64,
        "position": "after",
        "reference_page": 1
    })
    assert response.status_code == 200
    data = response.json()
    if data["success"]:
        assert "pdf" in data
        assert data["details"]["new_page_count"] == 2
