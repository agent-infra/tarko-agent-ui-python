#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Optimized Python package release script with branch management."""

import re
import subprocess
import sys
import os

import requests


def run_cmd(cmd, check=True):
    """Run command and optionally check return code."""
    print("🔧 {}".format(cmd))
    
    # Use Popen for compatibility
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    # Convert bytes to string for Python 2/3 compatibility
    if hasattr(stdout, 'decode'):
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
    
    # Create a simple result object
    class Result:
        def __init__(self, returncode, stdout, stderr):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr
    
    result = Result(process.returncode, stdout, stderr)
    
    if check and result.returncode != 0:
        print("❌ Command failed: {}".format(cmd))
        print("stdout: {}".format(result.stdout))
        print("stderr: {}".format(result.stderr))
        sys.exit(1)
    return result


def get_current_branch():
    """Get current git branch name."""
    result = run_cmd("git rev-parse --abbrev-ref HEAD")
    return result.stdout.strip()


def get_npm_latest_version():
    """Get latest npm version from registry."""
    print("🔍 Fetching latest npm version...")
    try:
        response = requests.get("https://registry.npmjs.org/@tarko/agent-ui-builder/latest", timeout=10)
        response.raise_for_status()
        version = response.json()["version"]
        print("📦 Latest npm version: {}".format(version))
        return version
    except requests.RequestException as e:
        print("❌ Failed to fetch npm version: {}".format(e))
        print("💡 You can specify --npm-version to use a specific version")
        sys.exit(1)


def get_current_python_version():
    """Get current Python version from pyproject.toml."""
    with open("pyproject.toml", "r") as f:
        content = f.read()
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def bump_patch_version(version):
    """Bump patch version: 0.3.0 -> 0.3.1"""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', version)
    if not match:
        raise ValueError("Invalid version format: {}".format(version))
    major, minor, patch = match.groups()
    return "{}.{}.{}".format(major, minor, int(patch) + 1)


def ensure_versions_consistent(python_version, npm_version):
    """Ensure Python and npm versions are consistent (same major.minor)."""
    py_match = re.match(r'^(\d+)\.(\d+)', python_version)
    npm_match = re.match(r'^(\d+)\.(\d+)', npm_version)
    
    if not py_match or not npm_match:
        raise ValueError("Invalid version format: Python={}, npm={}".format(python_version, npm_version))
    
    py_major_minor = "{}.{}".format(py_match.group(1), py_match.group(2))
    npm_major_minor = "{}.{}".format(npm_match.group(1), npm_match.group(2))
    
    if py_major_minor != npm_major_minor:
        print("⚠️  Version mismatch detected:")
        print("   Python: {} (major.minor: {})".format(python_version, py_major_minor))
        print("   npm: {} (major.minor: {})".format(npm_version, npm_major_minor))
        print("\n💡 Python and npm packages should have consistent major.minor versions")
        
        if input("❓ Continue anyway? [y/N]: ").lower() != "y":
            print("❌ Release cancelled due to version mismatch")
            sys.exit(1)
    else:
        print("✅ Version consistency check passed (major.minor: {})".format(py_major_minor))


def update_version_files(python_version, npm_version):
    """Update version in pyproject.toml and __init__.py."""
    print("📝 Updating version files: Python {}, npm {}".format(python_version, npm_version))
    
    # Update pyproject.toml
    with open("pyproject.toml", "r") as f:
        content = f.read()
    content = re.sub(r'version = "[^"]+"', 'version = "{}"'.format(python_version), content)
    with open("pyproject.toml", "w") as f:
        f.write(content)
    
    # Update __init__.py
    with open("tarko_agent_ui/__init__.py", "r") as f:
        content = f.read()
    content = re.sub(r'__version__ = "[^"]+"', '__version__ = "{}"'.format(python_version), content)
    content = re.sub(r'__npm_version__ = "[^"]+"', '__npm_version__ = "{}"'.format(npm_version), content)
    with open("tarko_agent_ui/__init__.py", "w") as f:
        f.write(content)
    
    print("✅ Version files updated")


def clean_old_artifacts():
    """Clean old build artifacts to ensure fresh build."""
    print("🧹 Cleaning old artifacts...")
    
    artifacts_to_clean = [
        "dist",
        "build", 
        "*.egg-info",
        "tarko_agent_ui/static",
        "tarko_agent_ui/_static_version.py",
        "tarko_agent_ui/__pycache__",
        ".pytest_cache"
    ]
    
    for artifact in artifacts_to_clean:
        run_cmd("rm -rf {}".format(artifact), check=False)
    
    # Also clean Python cache files
    run_cmd("find . -name '*.pyc' -delete", check=False)
    run_cmd("find . -name '__pycache__' -type d -exec rm -rf {} +", check=False)
    
    print("✅ Old artifacts cleaned")


def build_static_assets(npm_version):
    """Build static assets from npm package."""
    print("🏗️  Building static assets with npm version {}...".format(npm_version))
    run_cmd("uv run python scripts/build_assets.py --version='{}'".format(npm_version))
    
    # Verify static assets were built
    static_dir = "tarko_agent_ui/static"
    index_file = os.path.join(static_dir, "index.html")
    
    if not os.path.exists(static_dir) or not os.path.exists(index_file):
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
    if not os.path.exists("dist"):
        raise RuntimeError("Package build failed - dist directory not found")
    
    dist_files = os.listdir("dist")
    if not dist_files:
        raise RuntimeError("Package build failed - no files in dist/")
    
    print("✅ Package built successfully: {}".format(dist_files))


def create_release_branch(version):
    """Create and switch to release branch."""
    branch_name = "release/{}".format(version)
    print("🌿 Creating release branch: {}".format(branch_name))
    
    # Ensure we're on main and up to date
    run_cmd("git checkout main")
    run_cmd("git pull origin main")
    
    # Create and switch to release branch
    run_cmd("git checkout -b {}".format(branch_name))
    
    print("✅ Created and switched to branch: {}".format(branch_name))
    return branch_name


def commit_and_tag(version):
    """Commit changes and create git tag."""
    print("📝 Committing release v{}...".format(version))
    
    # Add all changes
    run_cmd("git add .")
    
    # Commit with conventional commit format
    run_cmd('git commit -m "release: v{}"'.format(version))
    
    # Create tag
    run_cmd("git tag v{}".format(version))
    
    print("✅ Committed and tagged v{}".format(version))


def push_release(version):
    """Push release branch and tags to remote."""
    branch_name = "release/{}".format(version)
    print("🚀 Pushing {} and tags...".format(branch_name))
    
    # Push branch
    run_cmd("git push origin {}".format(branch_name))
    
    # Push tags
    run_cmd("git push origin --tags")
    
    print("✅ Pushed {} and tags to remote".format(branch_name))


def switch_back_to_original_branch(original_branch):
    """Switch back to the original branch."""
    print("🔄 Switching back to original branch: {}".format(original_branch))
    run_cmd("git checkout {}".format(original_branch))
    print("✅ Switched back to {}".format(original_branch))


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
        print("🎯 Starting release from branch: {}".format(original_branch))
        
        # 2. Determine versions
        npm_version = args.npm_version or get_npm_latest_version()
        current_python_version = get_current_python_version()
        new_python_version = bump_patch_version(current_python_version)
        
        # 3. Check version consistency
        ensure_versions_consistent(new_python_version, npm_version)
        
        print("\n📋 Release Plan:")
        print("   📦 npm version: {}".format(npm_version))
        print("   🐍 Python: {} -> {}".format(current_python_version, new_python_version))
        print("   🌿 Release branch: release/{}".format(new_python_version))
        print("   🔗 Version consistency: ✅")
        
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
                
                # 13. Show testing instructions
                print("\n🧪 Testing Instructions:")
                print("   Run: python scripts/test_release.py --version {}".format(new_python_version))
                print("   Or quick test: python scripts/test_release.py --version {} --quick".format(new_python_version))
            
            print("\n🎉 Successfully released v{}!".format(new_python_version))
            print("📦 npm version: {}".format(npm_version))
            print("🐍 Python version: {}".format(new_python_version))
            print("🌿 Release branch: release/{}".format(new_python_version))
            
        finally:
            # 14. Always switch back to original branch
            switch_back_to_original_branch(original_branch)
            
    except KeyboardInterrupt:
        print("\n❌ Release interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\n❌ Release failed: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
