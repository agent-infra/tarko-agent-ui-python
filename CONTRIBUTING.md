# Contributing Guide

## Development Setup

```bash
# Clone repository
git clone https://github.com/agent-infra/tarko-agent-ui-python.git
cd tarko-agent-ui-python

# Install dependencies
uv sync --dev

# Build static assets
uv run python scripts/build_assets.py
```

## Development Workflow

```bash
# Run tests
uv run pytest

# Format code
uv run black .

# Type check
uv run mypy .

# Build package
uv build
```

## Publishing

```bash
# Check if ready for release
uv run python scripts/check_release_ready.py

# If all checks pass, publish to PyPI
uv build
uv publish
```

## Release Management

### Automated Release (Latest Version)

```bash
# Auto-detect and publish latest @tarko/agent-ui-builder version
uv run python scripts/auto_release.py

# Preview what would be done without executing
uv run python scripts/auto_release.py --dry-run
```

### Manual Release (Specific Version)

```bash
# Release a specific npm version
uv run python scripts/auto_release.py --version "0.3.0-beta.9"

# Preview specific version release
uv run python scripts/auto_release.py --version "0.3.0-beta.10" --dry-run
```

### Release Process

The release script automatically:

1. **Version Management**: Converts npm version format to Python format
   - `0.3.0-beta.11` → `0.3.0b11`
   - `0.3.0-alpha.5` → `0.3.0a5`
   - `1.0.0` → `1.0.0`

2. **File Updates**: Updates version in all relevant files:
   - `pyproject.toml`
   - `tarko_agent_ui/__init__.py`
   - `tests/test_core.py`

3. **Asset Management**: Downloads specified version of static assets

4. **Quality Assurance**: Runs tests before publishing

5. **Publishing**: Builds and publishes to PyPI with proper git tagging


