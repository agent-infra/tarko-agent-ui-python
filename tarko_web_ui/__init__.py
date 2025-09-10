#!/usr/bin/env python3

"""Tarko Web UI SDK for managing static assets from @tarko/agent-ui-builder."""

from pathlib import Path
from typing import Optional

try:
    from ._static_version import STATIC_ASSETS_VERSION, STATIC_ASSETS_PACKAGE
except ImportError:
    # Fallback if version file doesn't exist (development mode)
    STATIC_ASSETS_VERSION = "unknown"
    STATIC_ASSETS_PACKAGE = "@tarko/agent-ui-builder"


__version__ = "0.3.0b11"
__all__ = ["get_static_path", "get_static_version"]


def get_static_path() -> str:
    """Get the path to the static assets directory.
    
    Returns:
        str: Absolute path to the static assets directory.
        
    Raises:
        FileNotFoundError: If static assets are not found.
    """
    package_dir = Path(__file__).parent
    static_dir = package_dir / "static"
    
    if not static_dir.exists():
        raise FileNotFoundError(
            f"Static assets not found at {static_dir}. "
            "This package may not have been built properly. "
            "Please run: python scripts/build_assets.py"
        )
    
    # Verify essential files exist
    index_file = static_dir / "index.html"
    if not index_file.exists():
        raise FileNotFoundError(
            f"index.html not found in {static_dir}. "
            "Static assets may be incomplete. "
            "Please run: python scripts/build_assets.py"
        )
    
    return str(static_dir.absolute())


def get_static_version() -> dict:
    """Get information about the packaged static assets.
    
    Returns:
        dict: Information about the static assets including version and package name.
    """
    return {
        "version": STATIC_ASSETS_VERSION,
        "package": STATIC_ASSETS_PACKAGE,
        "sdk_version": __version__
    }
