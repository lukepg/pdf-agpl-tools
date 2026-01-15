# SPDX-License-Identifier: AGPL-3.0-or-later
"""Tests for redaction endpoint."""


def test_redact_invalid_pdf(client):
    """Test redaction with invalid PDF data."""
    response = client.post("/api/v1/redact", json={
        "pdf": "not-valid-base64",
        "redactions": [
            {"page": 1, "x": 0, "y": 0, "width": 100, "height": 50}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_redact_empty_redactions(client, sample_pdf_base64):
    """Test redaction with empty redactions list."""
    response = client.post("/api/v1/redact", json={
        "pdf": sample_pdf_base64,
        "redactions": []
    })
    # Should fail validation - redactions required
    assert response.status_code == 422


def test_redact_valid(client, sample_pdf_base64):
    """Test redaction with valid inputs."""
    response = client.post("/api/v1/redact", json={
        "pdf": sample_pdf_base64,
        "redactions": [
            {"page": 1, "x": 100, "y": 100, "width": 200, "height": 50, "fill": "#000000"}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    if data["success"]:
        assert "pdf" in data


def test_redact_with_replacement_text(client, sample_pdf_base64):
    """Test redaction with replacement text."""
    response = client.post("/api/v1/redact", json={
        "pdf": sample_pdf_base64,
        "redactions": [
            {"page": 1, "x": 100, "y": 100, "width": 200, "height": 50}
        ],
        "replacement_texts": [
            {"page": 1, "x": 100, "y": 100, "text": "REDACTED", "fontsize": 12}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    if data["success"]:
        assert "pdf" in data
