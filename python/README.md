# Tarko Agent UI FastAPI Example

A Python SDK and FastAPI example for serving static assets from the [`@tarko/agent-ui-builder`](https://www.npmjs.com/package/@tarko/agent-ui-builder) npm package.

## Features

- 🚀 Automatic download and extraction of `@tarko/agent-ui-builder` static assets
- 📦 Simple Python SDK with `get_static_path()` method
- 🌐 FastAPI server example for serving the web UI
- 🔧 Post-install automation for seamless setup

## Installation

```bash
cd python
pip install -e .
```

The static assets from `@tarko/agent-ui-builder` will be automatically downloaded during installation.

## Usage

### Python SDK

```python
from agent_sandbox import get_static_path

# Get the path to static assets
static_path = get_static_path()
print(f"Static assets located at: {static_path}")
```

### Manual Asset Download

If automatic download fails during installation:

```python
from agent_sandbox import download_static_assets

# Manually download static assets
download_static_assets()
```

### FastAPI Server Example

Run the example FastAPI server:

```bash
cd python/examples
python fastapi_server.py
```

Or using uvicorn directly:

```bash
cd python/examples
uvicorn fastapi_server:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at:
- Main UI: http://localhost:8000
- Health check: http://localhost:8000/health
- Static files: http://localhost:8000/static/

## Project Structure

```
python/
├── agent_sandbox/           # Main SDK package
│   ├── __init__.py         # SDK with get_static_path() and download_static_assets()
│   └── static/             # Downloaded static assets (created during install)
├── examples/
│   └── fastapi_server.py   # FastAPI server example
├── setup.py                # Setup with post-install hook
├── pyproject.toml          # Modern Python project configuration
└── README.md               # This file
```

## API Reference

### `get_static_path() -> str`

Returns the absolute path to the static assets directory.

**Returns:** Absolute path to static assets

**Raises:** `FileNotFoundError` if static assets are not found

### `download_static_assets() -> None`

Downloads and extracts the latest `@tarko/agent-ui-builder` package from npm registry.

**Raises:** `Exception` if download or extraction fails

## Requirements

- Python 3.7+
- Internet connection (for downloading npm package)
- FastAPI and Uvicorn (automatically installed)

## Development

For development installation:

```bash
cd python
pip install -e .
```

This installs the package in editable mode with automatic asset download.
