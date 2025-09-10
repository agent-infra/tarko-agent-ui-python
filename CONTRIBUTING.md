# Contributing to Tarko Agent UI Python SDK

## Development Setup

```bash
# Clone and setup
git clone https://github.com/agent-infra/tarko-agent-ui-python.git
cd tarko-agent-ui-python
uv sync --dev

# Build static assets
uv run python scripts/build_assets.py

# Run tests
uv run pytest
```

## Code Quality

```bash
# Format code
uv run black .

# Type checking
uv run mypy .

# Run tests with coverage
uv run pytest --cov=tarko_agent_ui
```

## Making Changes

1. **Fork and Clone**: Fork the repo and clone your fork
2. **Branch**: Create a feature branch (`git checkout -b feature/amazing-feature`)
3. **Develop**: Make your changes
4. **Test**: Ensure tests pass
5. **Commit**: Use conventional commits (`feat:`, `fix:`, `docs:`)
6. **Push**: Push to your fork and create a pull request

## Static Assets

Static assets are downloaded from `@tarko/agent-ui-builder` npm package:

```bash
# Rebuild assets
uv run python scripts/build_assets.py

# Download specific version
uv run python scripts/build_assets.py --version 0.3.0-beta.11
```

**Important**: Never manually edit files in `tarko_agent_ui/static/` - they are auto-generated.

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/agent-infra/tarko-agent-ui-python/issues)
- **Documentation**: Check README.md
