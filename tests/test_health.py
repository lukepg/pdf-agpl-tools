# SPDX-License-Identifier: AGPL-3.0-or-later
"""Tests for health check endpoint."""


def test_health_endpoint(client):
    """Test that health endpoint returns expected structure."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] in ["healthy", "degraded", "unhealthy"]
    assert "services" in data
    assert "pymupdf" in data["services"]
    assert "ghostscript" in data["services"]
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test that root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["service"] == "pdf-agpl-tools"
    assert "version" in data
    assert data["license"] == "AGPL-3.0-or-later"
    assert "source_code" in data


def test_source_code_header(client):
    """Test that X-Source-Code header is present in responses."""
    response = client.get("/api/v1/health")
    assert "X-Source-Code" in response.headers
