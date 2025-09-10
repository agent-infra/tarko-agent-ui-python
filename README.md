# Tarko Agent UI Python SDK

Python SDK for serving [`@tarko/agent-ui-builder`](https://www.npmjs.com/package/@tarko/agent-ui-builder) static assets.

## Installation

```bash
# Install from PyPI
pip install tarko-agent-ui

# Or with uv
uv add tarko-agent-ui
```

## Quick Start

### Option 1: Use the Package Directly

```python
from tarko_agent_ui import get_static_path
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
from tarko_agent_ui import get_static_path, inject_env_variables

# Get path to static files (for mounting in your web framework)
static_path = get_static_path()

# Inject environment variables into HTML
html_content = "<html><head></head><body></body></html>"
modified_html = inject_env_variables(
    html_content=html_content,
    base_url="http://localhost:8000/api",
    ui_config={"title": "My Agent", "logo": "logo.png"}
)
```

## Framework Integration

### FastAPI
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from tarko_agent_ui import get_static_path, inject_env_variables
from pathlib import Path

app = FastAPI()
app.mount("/static", StaticFiles(directory=get_static_path()))

@app.get("/", response_class=HTMLResponse)
async def root():
    # Read and inject environment variables into HTML
    index_file = Path(get_static_path()) / "index.html"
    html_content = index_file.read_text(encoding="utf-8")
    
    return inject_env_variables(
        html_content=html_content,
        base_url="http://localhost:8000/api",
        ui_config={"title": "My Agent", "logo": "logo.png"}
    )
```

### Flask
```python
from flask import Flask, send_from_directory
from tarko_agent_ui import get_static_path

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
