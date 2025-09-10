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

## Automated Release

```bash
# Auto-bump version and publish when @tarko/agent-ui-builder updates
uv run python scripts/auto_release.py
```
