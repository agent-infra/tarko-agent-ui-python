#!/usr/bin/env python3

"""Integration tests for FastAPI example."""

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Add examples directory to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))

try:
    from fastapi_server import create_app, handle_missing_assets
except ImportError:
    pytest.skip("FastAPI example not available", allow_module_level=True)


class TestFastAPIIntegration:
    """Test FastAPI integration."""

    def test_create_app_basic(self):
        """Test basic app creation."""
        with patch("fastapi_server.get_static_path") as mock_get_path:
            mock_get_path.return_value = "/mock/static"
            app = create_app()
            assert app is not None
            assert app.title == "Tarko Agent UI Server"

    def test_create_app_with_config(self):
        """Test app creation with configuration."""
        with patch("fastapi_server.get_static_path") as mock_get_path:
            mock_get_path.return_value = "/mock/static"

            ui_config = {"title": "Test Agent"}
            app = create_app(base_url="http://test.com", ui_config=ui_config)
            assert app is not None

    def test_health_endpoint(self):
        """Test health check endpoint."""
        with patch("fastapi_server.get_static_path") as mock_get_path:
            mock_get_path.return_value = "/mock/static"

            app = create_app()
            client = TestClient(app)
            response = client.get("/api/v1/health")

            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

    def test_root_endpoint_with_mock_assets(self):
        """Test root endpoint with mocked static assets."""
        mock_html = "<html><head></head><body>Test</body></html>"

        with patch("fastapi_server.get_static_path") as mock_get_path, patch(
            "fastapi_server.get_agent_ui_html"
        ) as mock_get_html:

            mock_get_path.return_value = "/mock/static"
            mock_get_html.return_value = mock_html

            app = create_app(base_url="http://test.com")
            client = TestClient(app)
            response = client.get("/")

            assert response.status_code == 200
            assert "Test" in response.text

    def test_root_endpoint_missing_assets(self):
        """Test root endpoint behavior when assets are missing."""
        with patch("fastapi_server.get_static_path") as mock_get_path, patch(
            "fastapi_server.get_agent_ui_html"
        ) as mock_get_html:

            mock_get_path.return_value = "/mock/static"
            mock_get_html.side_effect = FileNotFoundError("Assets not found")

            app = create_app()
            client = TestClient(app)
            response = client.get("/")

            assert response.status_code == 500
            assert "error" in response.json()

    def test_handle_missing_assets_api_context(self):
        """Test error handling for API context."""
        error = FileNotFoundError("Test error")

        with pytest.raises(Exception):  # HTTPException
            handle_missing_assets(error, "api")

    def test_handle_missing_assets_startup_context(self, capsys):
        """Test error handling for startup context."""
        error = FileNotFoundError("Test error")

        handle_missing_assets(error, "startup")
        captured = capsys.readouterr()

        assert "Test error" in captured.out
        assert "Run 'python scripts/build_assets.py'" in captured.out
