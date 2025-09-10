# Tarko Agent UI Python SDK

Python SDK for serving [`@tarko/agent-ui-builder`](https://www.npmjs.com/package/@tarko/agent-ui-builder) static assets.

## Installation

```bash
# Install from PyPI
pip install tarko-web-ui

# Or with uv
uv add tarko-web-ui
```

## Quick Start

### Option 1: Use the Package Directly

```python
from tarko_web_ui import get_static_path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory=get_static_path()))
```

### Option 2: Try the Example

```bash
# 1. Clone the example repository
git clone https://github.com/agent-infra/tarko-agent-ui-python.git
cd tarko-agent-ui-python
uv sync

# 2. Run the demo server
python3 examples/fastapi_server.py
# Open http://localhost:8000
```

## Core API

```python
from tarko_web_ui import get_static_path

# Get path to static files (for mounting in your web framework)
static_path = get_static_path()
```

## Framework Integration

### FastAPI
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tarko_web_ui import get_static_path

app = FastAPI()
app.mount("/static", StaticFiles(directory=get_static_path()))
```

### Flask
```python
from flask import Flask, send_from_directory
from tarko_web_ui import get_static_path

app = Flask(__name__)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(get_static_path(), filename)
```

## How It Works

1. **Package Installation**: Static assets are bundled with the Python package
2. **Runtime**: `get_static_path()` returns local path to pre-built assets
3. **Zero Overhead**: No runtime downloads, no npm dependencies

## Examples

- [`examples/fastapi_server.py`](examples/fastapi_server.py) - Complete FastAPI server with health check

## Requirements

- Python 3.8+
- Internet connection (for building assets)
