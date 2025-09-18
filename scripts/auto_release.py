#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Ultra-simple release script: bump patch version + record npm version."""

import re
import subprocess
import sys
from pathlib import Path

import requests


def get_npm_latest_version() -> str:
    """Get latest npm version."""
    response = requests.get("https://registry.npmjs.org/@tarko/agent-ui-builder/latest")
    return response.json()["version"]


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    content = Path("pyproject.toml").read_text()
    return re.search(r'version = "([^"]+)"', content).group(1)


def bump_patch_version(version: str) -> str:
    """Bump patch version: 0.3.0 -> 0.3.1"""
    # Extract x.y.z from complex versions like 0.3.0b12.post1
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', version)
    if not match:
        raise ValueError(f"Invalid version: {version}")
    major, minor, patch = match.groups()
    return f"{major}.{minor}.{int(patch) + 1}"


def update_version_files(new_version: str, npm_version: str):
    """Update version in all files."""
    # pyproject.toml
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()
    content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)
    pyproject.write_text(content)
    
    # __init__.py
    init_file = Path("tarko_agent_ui/__init__.py")
    content = init_file.read_text()
    content = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{new_version}"', content)
    content = re.sub(r'__npm_version__ = "[^"]+"', f'__npm_version__ = "{npm_version}"', content)
    init_file.write_text(content)


def run(cmd: str):
    """Run command or exit on failure."""
    if subprocess.run(cmd, shell=True).returncode != 0:
        sys.exit(1)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--npm-version", help="Specific npm version")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Get versions
    npm_version = args.npm_version or get_npm_latest_version()
    current_version = get_current_version()
    new_version = bump_patch_version(current_version)
    
    print(f"📦 npm: {npm_version}")
    print(f"🐍 {current_version} -> {new_version}")
    
    if args.dry_run:
        print("DRY RUN - would execute release")
        return
    
    if input("Release? [y/N]: ").lower() != "y":
        return
    
    # Release
    update_version_files(new_version, npm_version)
    run(f"uv run python scripts/build_assets.py --version='{npm_version}'")
    run("uv run pytest")
    run("uv build")
    run("uv publish")
    run(f"git add . && git commit -m 'release: v{new_version}'")
    run(f"git tag v{new_version} && git push origin main --tags")
    
    print(f"🎉 Released v{new_version}!")


if __name__ == "__main__":
    main()
