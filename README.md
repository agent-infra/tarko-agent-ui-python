# Tarko Web UI

Python SDK and FastAPI server for serving static web assets from [`@tarko/agent-ui-builder`](https://www.npmjs.com/package/@tarko/agent-ui-builder).

## Quick Start

```bash
# Install with uv (recommended)
uv add tarko-web-ui

# Or with pip
pip install tarko-web-ui

# Download static assets
tarko-web-ui download

# Start the server
tarko-web-ui serve
```

Visit http://localhost:8000 to access the Tarko Agent UI.

## Features

- 🚀 **Modern Python packaging** with `uv` and `pyproject.toml`
- 📦 **Clean API**: `get_static_path()` for easy integration
- 🌐 **Built-in server**: FastAPI server with CLI commands
- 🔧 **Flexible deployment**: Use as SDK or standalone server
- ⚡ **Fast setup**: Automatic asset download during build

## Installation

### Using uv (recommended)

```bash
uv add tarko-web-ui
```

### Using pip

```bash
pip install tarko-web-ui
```

## CLI Usage

```bash
# Download static assets
tarko-web-ui download

# Download specific version
tarko-web-ui download --version 0.3.0-beta.11

# Show static assets path
tarko-web-ui path

# Start development server
tarko-web-ui serve

# Start server with custom settings
tarko-web-ui serve --host 127.0.0.1 --port 3000 --reload
```

## SDK Usage

```python
from tarko_web_ui import get_static_path, download_static_assets

# Get static assets path
static_path = get_static_path()
print(f"Static assets: {static_path}")

# Download assets programmatically
download_static_assets()

# Download specific version
download_static_assets(version="0.3.0-beta.11")
```

## FastAPI Integration

```python
from tarko_web_ui.server import create_app
import uvicorn

# Create FastAPI app
app = create_app()

# Run with uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Project Structure

```
├── tarko_web_ui/           # Main package
│   ├── __init__.py        # Core SDK functions
│   ├── cli.py             # CLI commands
│   ├── server.py          # FastAPI server
│   └── static/            # Downloaded assets (auto-created)
├── examples/
│   └── fastapi_server.py  # Simple server example
├── pyproject.toml         # Modern Python config with uv support
├── build_hook.py          # Build-time asset download
└── README.md
```

## API Reference

### `get_static_path() -> str`

Returns absolute path to static assets directory.

**Raises:** `FileNotFoundError` if assets not downloaded

### `download_static_assets(version: Optional[str] = None) -> None`

Downloads and extracts static assets from npm registry.

**Args:**
- `version`: Specific version to download (default: latest)

**Raises:** `Exception` if download fails

## Development

```bash
# Clone repository
git clone https://github.com/agent-infra/tarko-agent-ui-fastapi-example.git
cd tarko-agent-ui-fastapi-example

# Install with uv
uv sync

# Or create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Download assets
tarko-web-ui download

# Run example
python examples/fastapi_server.py
```

## Requirements

- Python 3.8+
- Internet connection (for downloading npm package)
- FastAPI and Uvicorn (automatically installed)

## License

MIT License
