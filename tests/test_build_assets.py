#!/usr/bin/env python3

"""Tests for build_assets.py script."""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

# Add scripts directory to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from build_assets import (
        create_version_file,
        download_npm_package,
        get_project_paths,
    )
except ImportError:
    pytest.skip("Build assets script not available", allow_module_level=True)


class TestGetProjectPaths:
    """Test get_project_paths function."""

    def test_project_paths_structure(self):
        """Test that project paths are returned correctly."""
        project_root, package_dir = get_project_paths()

        assert isinstance(project_root, Path)
        assert isinstance(package_dir, Path)
        assert package_dir.name == "tarko_agent_ui"
        assert package_dir.parent == project_root


class TestCreateVersionFile:
    """Test create_version_file function."""

    def test_create_version_file_content(self):
        """Test version file creation with correct content."""
        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir)
            create_version_file("1.2.3", target_dir)

            version_file = target_dir / "_static_version.py"
            assert version_file.exists()

            content = version_file.read_text()
            assert 'STATIC_ASSETS_VERSION = "1.2.3"' in content
            assert 'STATIC_ASSETS_PACKAGE = "@tarko/agent-ui-builder"' in content

    def test_create_version_file_default_target(self):
        """Test version file creation with default target directory."""
        with patch("build_assets.get_project_paths") as mock_get_paths:
            mock_project_root = MagicMock()
            mock_package_dir = MagicMock()
            mock_get_paths.return_value = (mock_project_root, mock_package_dir)

            with patch("build_assets.Path.write_text") as mock_write:
                create_version_file("1.2.3")

                # Verify write_text was called
                mock_write.assert_called_once()
                content = mock_write.call_args[0][0]
                assert 'STATIC_ASSETS_VERSION = "1.2.3"' in content


class TestDownloadNpmPackage:
    """Test download_npm_package function."""

    def test_download_package_mock_registry(self):
        """Test package download with mocked registry response."""
        mock_package_info: dict = {
            "dist-tags": {"latest": "1.2.3"},
            "versions": {
                "1.2.3": {"dist": {"tarball": "https://registry.npmjs.org/package.tgz"}}
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir) / "static"

            with patch("build_assets.urlopen") as mock_urlopen, patch(
                "build_assets.tarfile.open"
            ) as mock_tarfile:

                # Mock registry response
                mock_response = MagicMock()
                mock_response.read.return_value = json.dumps(mock_package_info).encode()
                mock_urlopen.return_value.__enter__.return_value = mock_response

                # Mock tarfile extraction
                mock_tar = MagicMock()
                mock_member = MagicMock()
                mock_member.name = "package/static/index.html"
                mock_tar.getmembers.return_value = [mock_member]
                mock_tarfile.return_value.__enter__.return_value = mock_tar

                version = download_npm_package(target_dir=target_dir)

                assert version == "1.2.3"
                assert target_dir.exists()

    def test_download_package_specific_version(self):
        """Test package download with specific version."""
        mock_package_info: dict = {
            "versions": {
                "1.0.0": {
                    "dist": {"tarball": "https://registry.npmjs.org/package-1.0.0.tgz"}
                }
            }
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir) / "static"

            with patch("build_assets.urlopen") as mock_urlopen, patch(
                "build_assets.tarfile.open"
            ) as mock_tarfile:

                # Mock registry response
                mock_response = MagicMock()
                mock_response.read.return_value = json.dumps(mock_package_info).encode()
                mock_urlopen.return_value.__enter__.return_value = mock_response

                # Mock tarfile extraction
                mock_tar = MagicMock()
                mock_tar.getmembers.return_value = []
                mock_tarfile.return_value.__enter__.return_value = mock_tar

                version = download_npm_package(version="1.0.0", target_dir=target_dir)

                assert version == "1.0.0"

    def test_download_package_version_not_found(self):
        """Test package download with non-existent version."""
        mock_package_info: dict = {"versions": {"1.0.0": {}}}

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir) / "static"

            with patch("build_assets.urlopen") as mock_urlopen:
                mock_response = MagicMock()
                mock_response.read.return_value = json.dumps(mock_package_info).encode()
                mock_urlopen.return_value.__enter__.return_value = mock_response

                with pytest.raises(ValueError, match="Version 2.0.0 not found"):
                    download_npm_package(version="2.0.0", target_dir=target_dir)
