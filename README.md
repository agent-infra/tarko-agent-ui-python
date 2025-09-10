# Tarko Agent UI FastAPI Example

A Python SDK and FastAPI example for serving static web assets from the [`@tarko/agent-ui-builder`](https://www.npmjs.com/package/@tarko/agent-ui-builder) npm package.

## Quick Start

```bash
# Install the Python SDK
cd python
pip install -e .

# Run the FastAPI example
cd examples
python fastapi_server.py
```

Visit http://localhost:8000 to see the Tarko Agent UI.

## Features

- 🚀 **Automatic Asset Management**: Downloads and extracts `@tarko/agent-ui-builder` static assets during installation
- 📦 **Simple Python SDK**: Provides `get_static_path()` method for easy integration
- 🌐 **FastAPI Example**: Ready-to-use server implementation
- 🔧 **Zero Configuration**: Works out of the box with post-install automation

## Project Structure

```
├── python/                     # Python SDK and examples
│   ├── agent_sandbox/          # Main SDK package
│   │   ├── __init__.py        # SDK with get_static_path() method
│   │   └── static/            # Downloaded static assets (auto-created)
│   ├── examples/
│   │   └── fastapi_server.py  # FastAPI server example
│   ├── setup.py               # Setup with post-install hook
│   ├── pyproject.toml         # Modern Python project config
│   └── README.md              # Detailed documentation
└── README.md                   # This file
```

## Documentation

See [`python/README.md`](python/README.md) for detailed documentation, API reference, and usage examples.

## Requirements

- Python 3.7+
- Internet connection (for downloading npm package)
- FastAPI and Uvicorn (automatically installed)

## License

MIT License
