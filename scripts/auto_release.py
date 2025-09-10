#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Automated release script for tarko-agent-ui package.

Checks for new @tarko/agent-ui-builder versions and automatically:
1. Downloads latest assets
2. Bumps package version
3. Builds and publishes to PyPI
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

import requests


def get_npm_latest_version(package: str) -> Optional[str]:
    """Get latest version of npm package."""
    try:
        response = requests.get(f"https://registry.npmjs.org/{package}/latest")
        response.raise_for_status()
        return response.json()["version"]
    except Exception as e:
        print(f"❌ Failed to get npm version: {e}")
        return None


def get_current_python_version() -> Optional[str]:
    """Get current Python package version from pyproject.toml."""
    try:
        pyproject_path = Path("pyproject.toml")
        content = pyproject_path.read_text()
        match = re.search(r'version = "([^"]+)"', content)
        return match.group(1) if match else None
    except Exception as e:
        print(f"❌ Failed to get current version: {e}")
        return None


def normalize_npm_version_to_python(npm_version: str) -> str:
    """Convert npm version format to Python version format.

    Examples:
        0.3.0-beta.11 -> 0.3.0b11
        0.3.0-alpha.5 -> 0.3.0a5
        1.0.0 -> 1.0.0
    """
    # Handle beta versions: 0.3.0-beta.11 -> 0.3.0b11
    if "-beta." in npm_version:
        base, beta_num = npm_version.split("-beta.")
        return f"{base}b{beta_num}"

    # Handle alpha versions: 0.3.0-alpha.5 -> 0.3.0a5
    if "-alpha." in npm_version:
        base, alpha_num = npm_version.split("-alpha.")
        return f"{base}a{alpha_num}"

    # Handle rc versions: 0.3.0-rc.1 -> 0.3.0rc1
    if "-rc." in npm_version:
        base, rc_num = npm_version.split("-rc.")
        return f"{base}rc{rc_num}"

    # Regular version: 1.0.0 -> 1.0.0
    return npm_version


def should_update_version(current_python_version: str, npm_version: str) -> bool:
    """Check if Python package should be updated based on npm version."""
    target_python_version = normalize_npm_version_to_python(npm_version)
    return current_python_version != target_python_version


def update_version_in_pyproject(new_version: str) -> bool:
    """Update version in pyproject.toml."""
    try:
        pyproject_path = Path("pyproject.toml")
        content = pyproject_path.read_text()

        # Replace version
        new_content = re.sub(
            r'version = "[^"]+"', f'version = "{new_version}"', content
        )

        pyproject_path.write_text(new_content)
        return True
    except Exception as e:
        print(f"❌ Failed to update version: {e}")
        return False


def run_command(cmd: str) -> bool:
    """Run shell command and return success status."""
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"   Error: {e.stderr}")
        return False


def main():
    """Main release automation workflow."""
    print("🚀 Starting automated release process...")

    # Get versions
    npm_version = get_npm_latest_version("@tarko/agent-ui-builder")
    if not npm_version:
        sys.exit(1)

    current_version = get_current_python_version()
    if not current_version:
        sys.exit(1)

    print(f"📦 NPM version: {npm_version}")
    print(f"🐍 Current Python version: {current_version}")

    # Check if update needed
    if not should_update_version(current_version, npm_version):
        print("✅ Already up to date!")
        return

    # Generate new version (direct mapping)
    new_version = normalize_npm_version_to_python(npm_version)
    print(f"🔄 New version: {new_version}")

    # Confirm release
    confirm = input(f"\nProceed with release {new_version}? [y/N]: ")
    if confirm.lower() != "y":
        print("❌ Release cancelled")
        return

    # Release workflow
    steps = [
        "uv run python scripts/build_assets.py",  # Build assets
        f"git add . && git commit -m 'feat: update to @tarko/agent-ui-builder@{npm_version}'",
        "uv run pytest",  # Run tests
        "uv build",  # Build package
        "uv publish",  # Publish to PyPI
        f"git tag v{new_version}",  # Create git tag
        "git push origin main --tags",  # Push changes and tags
    ]

    # Update version first
    if not update_version_in_pyproject(new_version):
        sys.exit(1)

    print(f"\n📝 Updated version to {new_version}")

    # Execute release steps
    for step in steps:
        if not run_command(step):
            print(f"❌ Release failed at step: {step}")
            sys.exit(1)

    print(f"\n🎉 Successfully released {new_version}!")
    print(f"📦 Package: https://pypi.org/project/tarko-agent-ui/{new_version}/")


if __name__ == "__main__":
    main()
