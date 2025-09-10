# Tarko Web UI SDK

Minimal Python SDK for managing static assets from [`@tarko/agent-ui-builder`](https://www.npmjs.com/package/@tarko/agent-ui-builder).

## Philosophy

This package does **one thing well**: manages static assets from the npm package. It provides a clean API for other packages to consume these assets without imposing any server implementation.

**Auto-download**: Static assets are automatically downloaded on first use, eliminating manual setup steps.

## Quick Start

```bash
# Install the SDK (static assets download automatically)
uv add tarko-web-ui
# or: pip install tarko-web-ui

# Ready to use!
python -c "from tarko_web_ui import get_static_path; print(get_static_path())"
```

## Core API

### `get_static_path() -> str`

Returns the absolute path to static assets. **Automatically downloads assets if they don't exist.**

```python
from tarko_web_ui import get_static_path

static_path = get_static_path()  # Downloads assets on first call
print(f"Assets at: {static_path}")
```

**Raises:** `FileNotFoundError` if assets cannot be downloaded

### `download_static_assets(version: Optional[str] = None) -> None`

Downloads and extracts static assets from npm registry.

```python
from tarko_web_ui import download_static_assets

# Download latest version
download_static_assets()

# Download specific version
download_static_assets(version="0.3.0-beta.11")
```

**Args:**
- `version`: Specific version to download (default: latest)

**Raises:** `Exception` if download fails

## Integration Examples

### FastAPI

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tarko_web_ui import get_static_path

app = FastAPI()
static_path = get_static_path()
app.mount("/static", StaticFiles(directory=static_path))
```

### Flask

```python
from flask import Flask, send_from_directory
from tarko_web_ui import get_static_path

app = Flask(__name__)
static_path = get_static_path()

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(static_path, filename)
```

### Django

```python
# settings.py
from tarko_web_ui import get_static_path

STATICFILES_DIRS = [
    get_static_path(),
]
```

## Examples

See the [`examples/`](examples/) directory:

- [`simple_usage.py`](examples/simple_usage.py) - Basic SDK usage
- [`fastapi_server.py`](examples/fastapi_server.py) - Complete FastAPI integration

```bash
# Run the simple example
python examples/simple_usage.py

# Run the FastAPI server
uv run --with fastapi --with uvicorn python examples/fastapi_server.py
```

## Project Structure

```
├── tarko_web_ui/           # Core SDK package
│   ├── __init__.py        # Main API: get_static_path(), download_static_assets()
│   └── static/            # Downloaded assets (auto-created)
├── examples/              # Integration examples
│   ├── simple_usage.py    # Basic usage demo
│   └── fastapi_server.py  # Complete FastAPI server
├── pyproject.toml         # Modern Python config
├── uv.lock               # Reproducible dependencies
└── README.md
```

## Development

```bash
# Clone and setup
git clone https://github.com/agent-infra/tarko-agent-ui-fastapi-example.git
cd tarko-agent-ui-fastapi-example

# Install with development dependencies (assets download automatically)
uv sync

# Run examples
python examples/simple_usage.py
python examples/fastapi_server.py
```

## Design Principles

- **Single Responsibility**: Only manages static assets
- **Framework Agnostic**: Works with FastAPI, Flask, Django, etc.
- **Minimal Dependencies**: Zero runtime dependencies
- **Developer Friendly**: Clear error messages and examples

## Requirements

- Python 3.8+
- Internet connection (for downloading npm package)

## License

MIT License
