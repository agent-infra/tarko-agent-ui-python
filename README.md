# Tarko Web UI SDK

Python SDK for serving [`@tarko/agent-ui-builder`](https://www.npmjs.com/package/@tarko/agent-ui-builder) static assets.

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/agent-infra/tarko-agent-ui-fastapi-example.git
cd tarko-agent-ui-fastapi-example
uv sync

# 2. Build static assets
python scripts/build_assets.py

# 3. Run the demo
python examples/fastapi_server.py
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

1. **Build Time**: `scripts/build_assets.py` downloads npm package and extracts static files
2. **Runtime**: `get_static_path()` returns local path to pre-built assets
3. **Zero Overhead**: No runtime downloads, no npm dependencies

## Examples

- [`examples/simple_usage.py`](examples/simple_usage.py) - Basic usage
- [`examples/fastapi_server.py`](examples/fastapi_server.py) - Complete FastAPI server

## Requirements

- Python 3.8+
- Internet connection (for building assets)
