#!/usr/bin/env python3

"""Core functionality tests for tarko_agent_ui."""

import json
import tempfile
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from tarko_agent_ui import (
    get_agent_ui_html,
    get_static_path,
    get_static_version,
    inject_env_variables,
)


class TestGetStaticPath:
    """Test get_static_path function."""

    def test_static_path_exists(self):
        """Test that static path returns valid directory."""
        try:
            path = get_static_path()
            assert Path(path).exists()
            assert Path(path).is_dir()
        except FileNotFoundError:
            pytest.skip("Static assets not built")

    def test_static_path_missing_raises_error(self):
        """Test that missing static directory raises FileNotFoundError."""
        with patch("tarko_agent_ui.Path") as mock_path:
            mock_static_dir = mock_path.return_value.parent / "static"
            mock_static_dir.exists.return_value = False

            with pytest.raises(FileNotFoundError, match="Static assets not found"):
                get_static_path()

    def test_missing_index_html_raises_error(self):
        """Test that missing index.html raises FileNotFoundError."""
        with patch("tarko_agent_ui.Path") as mock_path:
            mock_static_dir = mock_path.return_value.parent / "static"
            mock_static_dir.exists.return_value = True
            mock_index_file = mock_static_dir / "index.html"
            mock_index_file.exists.return_value = False

            with pytest.raises(FileNotFoundError, match="index.html not found"):
                get_static_path()


class TestGetStaticVersion:
    """Test get_static_version function."""

    def test_version_info_structure(self):
        """Test that version info has correct structure."""
        version_info = get_static_version()

        assert isinstance(version_info, dict)
        assert "version" in version_info
        assert "package" in version_info
        assert "sdk_version" in version_info
        assert version_info["package"] == "@tarko/agent-ui-builder"
        assert version_info["sdk_version"] == "0.3.0b11"


class TestInjectEnvVariables:
    """Test inject_env_variables function."""

    def test_inject_basic_variables(self):
        """Test basic environment variable injection."""
        html = "<html><head></head><body></body></html>"
        result = inject_env_variables(html, "http://api.example.com")

        assert 'window.AGENT_BASE_URL = "http://api.example.com"' in result
        assert "window.AGENT_WEB_UI_CONFIG = {}" in result
        assert "console.log" in result

    def test_inject_with_ui_config(self):
        """Test injection with UI configuration."""
        html = "<html><head></head><body></body></html>"
        ui_config = {"title": "Test Agent", "theme": "dark"}
        result = inject_env_variables(html, "http://api.example.com", ui_config)

        assert 'window.AGENT_BASE_URL = "http://api.example.com"' in result
        assert '"title": "Test Agent"' in result
        assert '"theme": "dark"' in result

    def test_inject_with_complex_config(self):
        """Test injection with complex nested configuration."""
        html = "<html><head></head><body></body></html>"
        ui_config = {"nested": {"value": 123}, "array": [1, 2, 3], "boolean": True}
        result = inject_env_variables(html, "", ui_config)

        # Verify JSON serialization works correctly
        assert '"nested": {"value": 123}' in result
        assert '"array": [1, 2, 3]' in result
        assert '"boolean": true' in result

    def test_inject_missing_head_raises_error(self):
        """Test that HTML without head section raises ValueError."""
        html = "<html><body></body></html>"

        with pytest.raises(
            ValueError, match="HTML content must contain a valid <head> section"
        ):
            inject_env_variables(html, "http://api.example.com")

    def test_inject_case_insensitive_head(self):
        """Test that injection works with case-insensitive head tags."""
        html = "<html><HEAD></HEAD><body></body></html>"
        result = inject_env_variables(html, "http://api.example.com")

        assert "window.AGENT_BASE_URL" in result

    def test_inject_head_with_attributes(self):
        """Test injection works with head tag containing attributes."""
        html = '<html><head lang="en"></head><body></body></html>'
        result = inject_env_variables(html, "http://api.example.com")

        assert "window.AGENT_BASE_URL" in result

    def test_special_characters_in_config(self):
        """Test handling of special characters in configuration."""
        html = "<html><head></head><body></body></html>"
        ui_config = {
            "title": 'Agent with "quotes" & <tags>',
            "description": "Line 1\nLine 2",
        }
        result = inject_env_variables(html, "http://api.example.com", ui_config)

        # Verify JSON escaping works correctly
        assert '"Agent with \\"quotes\\" & <tags>"' in result
        assert '"Line 1\\nLine 2"' in result


class TestGetAgentUIHTML:
    """Test get_agent_ui_html function."""

    def test_html_generation_with_mock_file(self):
        """Test HTML generation with mocked static files."""
        mock_html = "<html><head></head><body>Test UI</body></html>"

        with patch("tarko_agent_ui.get_static_path") as mock_get_path, patch(
            "tarko_agent_ui.Path"
        ) as mock_path_class:

            mock_get_path.return_value = "/mock/static"
            mock_index_file = mock_path_class.return_value / "index.html"
            mock_index_file.exists.return_value = True
            mock_index_file.read_text.return_value = mock_html

            result = get_agent_ui_html("http://api.example.com", {"title": "Test"})

            assert 'window.AGENT_BASE_URL = "http://api.example.com"' in result
            assert '"title": "Test"' in result
            assert "Test UI" in result

    def test_html_missing_static_raises_error(self):
        """Test that missing static files raise FileNotFoundError."""
        with patch("tarko_agent_ui.get_static_path") as mock_get_path:
            mock_get_path.side_effect = FileNotFoundError("Static assets not found")

            with pytest.raises(FileNotFoundError):
                get_agent_ui_html()

    def test_html_missing_index_raises_error(self):
        """Test that missing index.html raises FileNotFoundError."""
        with patch("tarko_agent_ui.get_static_path") as mock_get_path, patch(
            "tarko_agent_ui.Path"
        ) as mock_path_class:

            mock_get_path.return_value = "/mock/static"
            mock_index_file = mock_path_class.return_value / "index.html"
            mock_index_file.exists.return_value = False

            with pytest.raises(
                FileNotFoundError, match="index.html not found in static assets"
            ):
                get_agent_ui_html()

    def test_html_invalid_content_raises_error(self):
        """Test that invalid HTML content raises ValueError."""
        mock_html = "<html><body>No head section</body></html>"

        with patch("tarko_agent_ui.get_static_path") as mock_get_path, patch(
            "tarko_agent_ui.Path"
        ) as mock_path_class:

            mock_get_path.return_value = "/mock/static"
            mock_index_file = mock_path_class.return_value / "index.html"
            mock_index_file.exists.return_value = True
            mock_index_file.read_text.return_value = mock_html

            with pytest.raises(
                ValueError, match="HTML content must contain a valid <head> section"
            ):
                get_agent_ui_html()
