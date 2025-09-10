#!/usr/bin/env python3

import os
import tempfile
import tarfile
import shutil
import json
import sys
from urllib.request import urlopen
from pathlib import Path


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
            "Please run: python -c 'from agent_sandbox import download_static_assets; download_static_assets()'"
        )
    
    return str(static_dir.absolute())


def download_static_assets() -> None:
    """Download and extract @tarko/agent-ui-builder npm package static assets.
    
    This function downloads the latest version of @tarko/agent-ui-builder
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
        
        # Get latest version tarball URL
        latest_version = package_info["dist-tags"]["latest"]
        tarball_url = package_info["versions"][latest_version]["dist"]["tarball"]
        
        print(f"Downloading {package_name}@{latest_version}...")
        
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
                        # Remove 'package/' prefix and extract to static_dir
                        relative_path = member.name[8:]  # len("package/") = 8
                        if relative_path and relative_path != "static/":
                            # Adjust the member name for extraction
                            member.name = relative_path
                            tar.extract(member, static_dir)
                            extracted_count += 1
        
        print(f"Successfully extracted {extracted_count} static files to {static_dir}")
        
    except Exception as e:
        print(f"Error downloading npm package: {e}", file=sys.stderr)
        raise


__all__ = ["get_static_path", "download_static_assets"]
