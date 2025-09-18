#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Optimized Python package release script with branch management."""

import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

import requests


def run_cmd(cmd, check=True):
    """Run command and optionally check return code."""
    print(f"🔧 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result


def get_current_branch():
    """Get current git branch name."""
    result = run_cmd("git rev-parse --abbrev-ref HEAD")
    return result.stdout.strip()


def get_npm_latest_version():
    """Get latest npm version from registry."""
    print("🔍 Fetching latest npm version...")
    response = requests.get("https://registry.npmjs.org/@tarko/agent-ui-builder/latest")
    response.raise_for_status()
    version = response.json()["version"]
    print(f"📦 Latest npm version: {version}")
    return version


def get_current_python_version():
    """Get current Python version from pyproject.toml."""
    content = Path("pyproject.toml").read_text()
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def bump_patch_version(version):
    """Bump patch version: 0.3.0 -> 0.3.1"""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch = match.groups()
    return f"{major}.{minor}.{int(patch) + 1}"


def update_version_files(python_version, npm_version):
    """Update version in pyproject.toml and __init__.py."""
    print(f"📝 Updating version files: Python {python_version}, npm {npm_version}")
    
    # Update pyproject.toml
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()
    content = re.sub(r'version = "[^"]+"', f'version = "{python_version}"', content)
    pyproject.write_text(content)
    
    # Update __init__.py
    init_file = Path("tarko_agent_ui/__init__.py")
    content = init_file.read_text()
    content = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{python_version}"', content)
    content = re.sub(r'__npm_version__ = "[^"]+"', f'__npm_version__ = "{npm_version}"', content)
    init_file.write_text(content)
    
    print("✅ Version files updated")


def clean_old_artifacts():
    """Clean old build artifacts to ensure fresh build."""
    print("🧹 Cleaning old artifacts...")
    
    # Remove dist directory
    run_cmd("rm -rf dist", check=False)
    
    # Remove build artifacts
    run_cmd("rm -rf build", check=False)
    run_cmd("rm -rf *.egg-info", check=False)
    
    # Remove static assets to force rebuild
    run_cmd("rm -rf tarko_agent_ui/static", check=False)
    run_cmd("rm -f tarko_agent_ui/_static_version.py", check=False)
    
    print("✅ Old artifacts cleaned")


def build_static_assets(npm_version):
    """Build static assets from npm package."""
    print(f"🏗️  Building static assets with npm version {npm_version}...")
    run_cmd(f"uv run python scripts/build_assets.py --version='{npm_version}'")
    
    # Verify static assets were built
    static_dir = Path("tarko_agent_ui/static")
    index_file = static_dir / "index.html"
    
    if not static_dir.exists() or not index_file.exists():
        raise RuntimeError("Static assets build failed - missing files")
    
    print("✅ Static assets built successfully")


def run_tests():
    """Run test suite to ensure everything works."""
    print("🧪 Running tests...")
    run_cmd("uv run pytest")
    print("✅ All tests passed")


def build_and_verify_package():
    """Build Python package and verify it can be published."""
    print("📦 Building Python package...")
    
    # Create dist directory
    run_cmd("mkdir -p dist")
    
    # Build package
    run_cmd("uv build")
    
    # Verify dist files exist
    dist_files = list(Path("dist").glob("*"))
    if not dist_files:
        raise RuntimeError("Package build failed - no files in dist/")
    
    print(f"✅ Package built successfully: {[f.name for f in dist_files]}")


def create_release_branch(version):
    """Create and switch to release branch."""
    branch_name = f"release/{version}"
    print(f"🌿 Creating release branch: {branch_name}")
    
    # Ensure we're on main and up to date
    run_cmd("git checkout main")
    run_cmd("git pull origin main")
    
    # Create and switch to release branch
    run_cmd(f"git checkout -b {branch_name}")
    
    print(f"✅ Created and switched to branch: {branch_name}")
    return branch_name


def commit_and_tag(version):
    """Commit changes and create git tag."""
    print(f"📝 Committing release v{version}...")
    
    # Add all changes
    run_cmd("git add .")
    
    # Commit with conventional commit format
    run_cmd(f'git commit -m "release: v{version}"')
    
    # Create tag
    run_cmd(f"git tag v{version}")
    
    print(f"✅ Committed and tagged v{version}")


def push_release(version):
    """Push release branch and tags to remote."""
    branch_name = f"release/{version}"
    print(f"🚀 Pushing {branch_name} and tags...")
    
    # Push branch
    run_cmd(f"git push origin {branch_name}")
    
    # Push tags
    run_cmd("git push origin --tags")
    
    print(f"✅ Pushed {branch_name} and tags to remote")


def switch_back_to_original_branch(original_branch):
    """Switch back to the original branch."""
    print(f"🔄 Switching back to original branch: {original_branch}")
    run_cmd(f"git checkout {original_branch}")
    print(f"✅ Switched back to {original_branch}")


def publish_package():
    """Publish package to PyPI."""
    print("🚀 Publishing to PyPI...")
    run_cmd("uv publish")
    print("✅ Package published to PyPI")


def main():
    """Main release workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimized Python package release script")
    parser.add_argument("--npm-version", help="Specific npm version (default: latest)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-publish", action="store_true", help="Skip publishing to PyPI")
    
    args = parser.parse_args()
    
    try:
        # 1. Get current state
        original_branch = get_current_branch()
        print(f"🎯 Starting release from branch: {original_branch}")
        
        # 2. Determine versions
        npm_version = args.npm_version or get_npm_latest_version()
        current_python_version = get_current_python_version()
        new_python_version = bump_patch_version(current_python_version)
        
        print(f"\n📋 Release Plan:")
        print(f"   📦 npm version: {npm_version}")
        print(f"   🐍 Python: {current_python_version} -> {new_python_version}")
        print(f"   🌿 Release branch: release/{new_python_version}")
        
        if args.dry_run:
            print("\n🔍 DRY RUN - No changes will be made")
            return
        
        # 3. Confirm release
        if input("\n❓ Proceed with release? [y/N]: ").lower() != "y":
            print("❌ Release cancelled")
            return
        
        print("\n🚀 Starting release process...")
        
        # 4. Create release branch
        create_release_branch(new_python_version)
        
        try:
            # 5. Clean old artifacts
            clean_old_artifacts()
            
            # 6. Update version files
            update_version_files(new_python_version, npm_version)
            
            # 7. Build static assets
            build_static_assets(npm_version)
            
            # 8. Run tests (unless skipped)
            if not args.skip_tests:
                run_tests()
            
            # 9. Build package
            build_and_verify_package()
            
            # 10. Commit and tag
            commit_and_tag(new_python_version)
            
            # 11. Push to remote
            push_release(new_python_version)
            
            # 12. Publish package (unless skipped)
            if not args.skip_publish:
                publish_package()
            
            print(f"\n🎉 Successfully released v{new_python_version}!")
            print(f"📦 npm version: {npm_version}")
            print(f"🐍 Python version: {new_python_version}")
            print(f"🌿 Release branch: release/{new_python_version}")
            
        finally:
            # 13. Always switch back to original branch
            switch_back_to_original_branch(original_branch)
            
    except KeyboardInterrupt:
        print("\n❌ Release interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Release failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
