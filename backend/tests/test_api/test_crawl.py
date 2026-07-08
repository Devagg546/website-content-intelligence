"""
Tests for crawl API endpoints.
"""

import pytest


class TestCrawlEndpoints:
    """Tests for /api/crawl endpoints."""

    def test_health_check(self, test_client):
        """Test the health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_start_crawl(self, test_client):
        """Test starting a crawl job."""
        response = test_client.post(
            "/api/crawl",
            json={"url": "https://example.com", "max_pages": 10},
        )
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "started"

    def test_start_crawl_invalid_url(self, test_client):
        """Test that invalid URLs are rejected."""
        # TODO: Add URL validation
        pass

    def test_get_crawl_status(self, test_client):
        """Test getting crawl job status."""
        response = test_client.get("/api/crawl/status/test-job-id")
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert "status" in data

    def test_get_crawl_history(self, test_client):
        """Test getting crawl history."""
        response = test_client.get("/api/crawl/history")
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
