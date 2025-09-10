# Contributing to Tarko Agent UI Python SDK

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/agent-infra/tarko-agent-ui-python.git
cd tarko-agent-ui-python

# Install dependencies
uv sync --dev

# Build static assets
uv run python scripts/build_assets.py

# Run tests
uv run pytest
```

## Code Quality

### Formatting and Linting

```bash
# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy .

# Run all checks
uv run black --check . && uv run isort --check-only . && uv run mypy .
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=tarko_agent_ui --cov-report=html

# Run specific test file
uv run pytest tests/test_core.py

# Run tests excluding slow ones
uv run pytest -m "not slow"
```

## Project Structure

```
├── tarko_agent_ui/          # Main package
│   ├── __init__.py          # Public API
│   ├── _static_version.py   # Auto-generated version info
│   └── static/              # Bundled web assets (auto-generated)
├── tests/                   # Test suite
├── examples/                # Usage examples
├── scripts/                 # Build and utility scripts
└── docs/                    # Documentation
```

## Making Changes

### Workflow

1. **Fork and Clone**: Fork the repo and clone your fork
2. **Branch**: Create a feature branch (`git checkout -b feature/amazing-feature`)
3. **Develop**: Make your changes following our guidelines
4. **Test**: Ensure all tests pass and add new tests for new functionality
5. **Commit**: Use conventional commits (`feat:`, `fix:`, `docs:`, etc.)
6. **Push**: Push to your fork and create a pull request

### Commit Convention

```bash
feat: add new UI configuration option
fix: resolve HTML injection issue
docs: update README examples
test: add integration tests
chore: update dependencies
```

### Adding Features

1. **API Design**: Ensure new APIs are intuitive and well-documented
2. **Type Safety**: Add proper type hints for all public APIs
3. **Error Handling**: Provide clear error messages with actionable suggestions
4. **Tests**: Add comprehensive tests covering edge cases
5. **Documentation**: Update README and docstrings

### Static Assets

Static assets are automatically downloaded from `@tarko/agent-ui-builder` npm package:

```bash
# Rebuild assets (downloads latest version)
uv run python scripts/build_assets.py

# Download specific version
uv run python scripts/build_assets.py --version 0.3.0-beta.11
```

**Important**: Never manually edit files in `tarko_agent_ui/static/` - they are auto-generated.

## Testing Guidelines

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Writing Tests

```python
def test_feature_behavior():
    """Test specific behavior with clear description."""
    # Arrange
    input_data = "test input"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == "expected output"
```

### Mocking External Dependencies

```python
from unittest.mock import patch, MagicMock

def test_with_external_dependency():
    with patch('module.external_function') as mock_func:
        mock_func.return_value = "mocked result"
        # Test logic here
```

## Documentation

### Docstring Format

```python
def function_name(param1: str, param2: Optional[int] = None) -> str:
    """Brief description of function purpose.
    
    Args:
        param1: Description of first parameter
        param2: Description of optional parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When input is invalid
        FileNotFoundError: When required files are missing
    """
```

### README Updates

When adding features:

1. Add usage examples
2. Update API reference
3. Add to table of contents if needed
4. Keep examples concise and practical

## Release Process

### Version Bumping

1. Update version in `pyproject.toml`
2. Update `__version__` in `tarko_agent_ui/__init__.py`
3. Update CHANGELOG.md
4. Create release PR

### Pre-release Checklist

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] Static assets are current
- [ ] Version numbers are consistent
- [ ] CHANGELOG.md is updated

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/agent-infra/tarko-agent-ui-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/agent-infra/tarko-agent-ui-python/discussions)
- **Documentation**: Check README.md and inline documentation

## Code of Conduct

Please be respectful and constructive in all interactions. We're building this together! 🚀
