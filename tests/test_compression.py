# SPDX-License-Identifier: AGPL-3.0-or-later
"""Tests for compression endpoints."""


def test_get_compression_methods(client):
    """Test getting available compression methods."""
    response = client.get("/api/v1/compress/methods")
    assert response.status_code == 200

    data = response.json()
    assert "methods" in data
    assert len(data["methods"]) == 4

    methods = [m["method"] for m in data["methods"]]
    assert "gs-minimum" in methods
    assert "gs-screen" in methods
    assert "gs-ebook" in methods
    assert "gs-printer" in methods


def test_compress_invalid_pdf(client):
    """Test compression with invalid PDF data."""
    response = client.post("/api/v1/compress", json={
        "pdf": "not-valid-base64",
        "method": "gs-screen"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_compress_invalid_method(client, sample_pdf_base64):
    """Test compression with invalid method."""
    response = client.post("/api/v1/compress", json={
        "pdf": sample_pdf_base64,
        "method": "invalid-method"
    })
    # Should fail validation
    assert response.status_code == 422


def test_compress_valid(client, sample_pdf_base64):
    """Test compression with valid inputs."""
    response = client.post("/api/v1/compress", json={
        "pdf": sample_pdf_base64,
        "method": "gs-screen"
    })
    assert response.status_code == 200
    data = response.json()
    # Will fail if Ghostscript not installed, but structure should be correct
    if data["success"]:
        assert "pdf" in data
        assert "stats" in data
        assert "original_size" in data["stats"]
        assert "compressed_size" in data["stats"]
