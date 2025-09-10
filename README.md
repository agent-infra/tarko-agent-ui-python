# Tarko Web UI SDK

Minimal Python SDK for managing static assets from [`@tarko/agent-ui-builder`](https://www.npmjs.com/package/@tarko/agent-ui-builder).

## Philosophy

This package does **one thing well**: manages static assets from the npm package. It provides a clean API for other packages to consume these assets without imposing any server implementation.

**Pre-built assets**: Static assets are downloaded and packaged during development, ensuring zero runtime overhead and version consistency.

## Quick Start

```bash
# Install the SDK (pre-built with static assets)
uv add tarko-web-ui
# or: pip install tarko-web-ui

# Ready to use immediately!
python -c "from tarko_web_ui import get_static_path; print(get_static_path())"
```

## Core API

### `get_static_path() -> str`

Returns the absolute path to pre-built static assets.

```python
from tarko_web_ui import get_static_path

static_path = get_static_path()  # No runtime download!
print(f"Assets at: {static_path}")
```

**Raises:** `FileNotFoundError` if assets weren't built properly

### `get_static_version() -> dict`

Returns version information about the packaged static assets.

```python
from tarko_web_ui import get_static_version

version_info = get_static_version()
print(f"Package: {version_info['package']}@{version_info['version']}")
print(f"SDK: {version_info['sdk_version']}")
```

**Returns:**
- `version`: npm package version (e.g., "0.3.0-beta.11")
- `package`: npm package name ("@tarko/agent-ui-builder")
- `sdk_version`: SDK version

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

- [`simple_usage.py`](examples/simple_usage.py) - Basic SDK usage with version info
- [`fastapi_server.py`](examples/fastapi_server.py) - Complete FastAPI integration

```bash
# Run the simple example
python examples/simple_usage.py

# Run the FastAPI server
uv run --with fastapi --with uvicorn python examples/fastapi_server.py
```

## Development Workflow

### Building Static Assets

```bash
# Download latest version
python scripts/build_assets.py

# Download specific version
python scripts/build_assets.py --version 0.3.0-beta.11

# Custom output directory
python scripts/build_assets.py --output ./custom/path
```

### Project Setup

```bash
# Clone and setup
git clone https://github.com/agent-infra/tarko-agent-ui-fastapi-example.git
cd tarko-agent-ui-fastapi-example

# Install with development dependencies
uv sync

# Build static assets
python scripts/build_assets.py

# Run examples
python examples/simple_usage.py
python examples/fastapi_server.py
```

## Project Structure

```
├── tarko_web_ui/              # Core SDK package
│   ├── __init__.py           # Main API: get_static_path(), get_static_version()
│   ├── _static_version.py    # Auto-generated version info
│   └── static/               # Pre-built static assets
├── scripts/
│   └── build_assets.py       # Asset build script
├── examples/                 # Integration examples
│   ├── simple_usage.py       # Basic usage demo
│   └── fastapi_server.py     # Complete FastAPI server
├── pyproject.toml            # Modern Python config
├── uv.lock                  # Reproducible dependencies
└── README.md
```

## Advantages

### ✅ Zero Runtime Overhead
- No network requests during application startup
- No dependency on npm registry availability
- Immediate asset access

### ✅ Version Management
- Explicit version tracking in `_static_version.py`
- Consistent assets across deployments
- Easy version auditing

### ✅ Distribution Ready
- Assets included in Python package
- Works in air-gapped environments
- No post-install scripts needed

### ✅ Developer Friendly
- Simple build script for asset updates
- Clear version information API
- Framework agnostic design

## Design Principles

- **Single Responsibility**: Only manages static assets
- **Framework Agnostic**: Works with FastAPI, Flask, Django, etc.
- **Zero Runtime Dependencies**: No external dependencies
- **Version Consistency**: Assets match npm package versions
- **Build-Time Download**: Assets prepared during development

## Requirements

- Python 3.8+
- Internet connection (for building assets only)

## License

MIT License
