# Release Scripts

This directory contains the automated release and testing scripts for the tarko-agent-ui Python package.

## Script Description

### 1. `auto_release.py` - Automatic Release Script

Optimized Python package release process, including the following features:

- ✅ Automatically determine the next version number (patch version increments)
- ✅ Create `release/{version}` branch
- ✅ Pull the latest npm package or a specified version
- ✅ Update version information in the code
- ✅ Automatically create a git tag
- ✅ Push to remote repository
- ✅ Publish to PyPI
- ✅ Automatically revert to the original branch
- ✅ Version consistency check
- ✅ Clean up old artifacts

#### Usage

```bash
# Basic release (using the latest npm version)
python scripts/auto_release.py

# Specify npm version
python scripts/auto_release.py --npm-version "0.3.0-beta.12"

# Preview mode (no actual changes)
python scripts/auto_release.py --dry-run

# Skip tests (for faster release)
python scripts/auto_release.py --skip-tests

# Skip publishing to PyPI (for release preparation only)
python scripts/auto_release.py --skip-publish

#### Release Process

1. **Version Check**: Get the current Python version and automatically bump the patch version
2. **npm Version**: Get the latest npm version or use a specified version
3. **Version Consistency**: Ensure the major and minor values ​​of the Python and npm versions are consistent
4. **Branch Management**: Create a `release/{version}` branch from `main`
5. **Clean**: Delete old build artifacts and static assets
6. **Update**: Update the versions in `pyproject.toml` and `__init__.py`
7. **Build**: Build static assets from the npm package
8. **Test**: Run the test suite (optional)
9. **Packaging**: Builds the Python package
10. **Commit**: Creates commits and git tags
11. **Push**: Pushes branches and tags to the remote repository
12. **Publish**: Publishes to PyPI (optional)
13. **Revert**: Switches back to the original branch

### 2. `test_release.py` - Release Test Script

Automated test script used to verify that the released package works properly.

#### Features

- ✅ Wait for PyPI package availability
- ✅ Create a clean test environment
- ✅ Install released packages
- ✅ Functional testing (imports, versions, static assets, HTML generation)
- ✅ Server testing (FastAPI integration)
- ✅ Automatically clean up the test environment

#### Usage

```bash
# Test the current version
python scripts/test_release.py

# Test a specific version
python scripts/test_release.py --version "0.3.5"

# Quick test (skips server testing)
python scripts/test_release.py --quick

# Skip waiting for PyPI to become available (if the package is already available)
python scripts/test_release.py --skip-wait

# Preserve the test environment (for debugging)
python scripts/test_release.py --keep-env

# Test a different package name
python scripts/test_release.py --package-name "my-package"
```

#### Test Content

**Functional Test**:
- Package import test
- Version information verification
- Static resource check
- HTML generation and environment variable injection

**Server Test**:
- FastAPI application startup
- Health check endpoint
- UI homepage responsiveness
- Static file serving

## Complete Release Workflow

```bash
# 1. Execute release
python scripts/auto_release.py

# 2. Test the release after waiting a few minutes
python scripts/test_release.py

# 3. If the tests pass, the release is complete!
```

## Version Management Strategy

- **Python Package Version**: Automatically bump patch versions (0.3.4 → 0.3.5)
- **npm Version**: Use the latest version or manually specify
- **Version Consistency**: Maintain the same major and minor versions for Python and npm packages
- **Branch Naming**: `release/{python_version}`
- **Tag Naming**: `v{python_version}`

## Troubleshooting

### Common Issues

**Version Inconsistency Warning**:
```
⚠️ Version mismatch detected:
Python: 0.4.1 (major.minor: 0.4)
npm: 0.3.0-beta.12 (major.minor: 0.3)
```
Solution: Use `--npm-version` to specify a matching npm version

**Static asset build failed**:
```
❌ Static assets build failed - missing files
```
Solution: Check `scripts/build_assets.py` and npm package availability

**PyPI release failed**:
```
❌ Package build failed - no files in dist/
```
Solution: Ensure `uv build` command is available and check `pyproject.toml` configuration

**Test environment creation failed**:
```
❌ Command failed: python -m venv test_env
```
Solution: Ensure the Python venv module is available

### Manual Cleanup

If the release process is interrupted, manual cleanup may be required:

```bash
# Delete the release branch
git branch -D release/0.3.5
git push origin --delete release/0.3.5

# Delete the tag
git tag -d v0.3.5
git push origin --delete v0.3.5

# Clean up build artifacts
rm -rf dist build *.egg-info
rm -rf tarko_agent_ui/static
rm -f tarko_agent_ui/_static_version.py
```

## Dependency Requirements

- Python 3.8+
- `uv` (for package management and builds)
- `requests` (for npm API calls)
- `git` (for version control)
- Network connection (for npm and PyPI access)

## Security Considerations

- Ensure PyPI credentials are correctly configured
- Review code changes before publishing
- Verify in a test environment before using in production
- Update dependency versions regularly