#!/usr/bin/env python3

"""Tarko Web UI SDK for managing static assets from @tarko/agent-ui-builder."""

import os
import tempfile
import tarfile
import shutil
import json
import sys
from urllib.request import urlopen
from pathlib import Path
from typing import Optional


__version__ = "0.1.0"
__all__ = ["get_static_path", "download_static_assets"]


def get_static_path() -> str:
    """Get the path to the static assets directory.
    
    Automatically downloads assets if they don't exist.
    
    Returns:
        str: Absolute path to the static assets directory.
        
    Raises:
        FileNotFoundError: If static assets cannot be downloaded.
    """
    package_dir = Path(__file__).parent
    static_dir = package_dir / "static"
    
    if not static_dir.exists() or not (static_dir / "index.html").exists():
        print("📦 Static assets not found, downloading automatically...")
        try:
            download_static_assets()
            print("✅ Static assets downloaded successfully!")
        except Exception as e:
            raise FileNotFoundError(
                f"Failed to download static assets: {e}. "
                "You can try manually: python -c 'from tarko_web_ui import download_static_assets; download_static_assets()'"
            )
    
    return str(static_dir.absolute())


def download_static_assets(version: Optional[str] = None) -> None:
    """Download and extract @tarko/agent-ui-builder npm package static assets.
    
    Args:
        version: Specific version to download. If None, downloads latest.
    
    This function downloads the specified version (or latest) of @tarko/agent-ui-builder
    from the npm registry and extracts the static assets to the local
    static directory.
    """
    package_name = "@tarko/agent-ui-builder"
    
    try:
        # Get package info from npm registry
        registry_url = f"https://registry.npmjs.org/{package_name.replace('@', '%40')}"
        print(f"Fetching package info from {registry_url}...")
        
        with urlopen(registry_url) as response:
            package_info = json.loads(response.read().decode())
        
        # Get version tarball URL
        if version is None:
            target_version = package_info["dist-tags"]["latest"]
        else:
            target_version = version
            
        if target_version not in package_info["versions"]:
            available_versions = list(package_info["versions"].keys())
            raise ValueError(
                f"Version {target_version} not found. Available versions: {available_versions}"
            )
            
        tarball_url = package_info["versions"][target_version]["dist"]["tarball"]
        
        print(f"Downloading {package_name}@{target_version}...")
        
        # Create static directory in package
        package_dir = Path(__file__).parent
        static_dir = package_dir / "static"
        
        # Clean existing static directory
        if static_dir.exists():
            shutil.rmtree(static_dir)
        static_dir.mkdir(parents=True, exist_ok=True)
        
        # Download and extract tarball
        with tempfile.NamedTemporaryFile(suffix=".tgz") as tmp_file:
            with urlopen(tarball_url) as response:
                shutil.copyfileobj(response, tmp_file)
            tmp_file.flush()
            
            # Extract static files
            with tarfile.open(tmp_file.name, "r:gz") as tar:
                extracted_count = 0
                for member in tar.getmembers():
                    if member.name.startswith("package/static/"):
                        # Remove 'package/static/' prefix and extract to static_dir
                        relative_path = member.name[15:]  # len("package/static/") = 15
                        if relative_path:  # Skip empty paths
                            # Create a new member with adjusted path
                            member.name = relative_path
                            tar.extract(member, static_dir)
                            extracted_count += 1
        
        print(f"Successfully extracted {extracted_count} static files to {static_dir}")
        
    except Exception as e:
        print(f"Error downloading npm package: {e}", file=sys.stderr)
        raise
