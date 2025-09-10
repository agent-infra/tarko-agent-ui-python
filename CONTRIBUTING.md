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
# Build and publish to PyPI
uv build
uv publish
```

## Project Structure

- `tarko_agent_ui/` - Main package code
- `scripts/build_assets.py` - Static asset builder
- `examples/` - Usage examples
- `tests/` - Test suite
