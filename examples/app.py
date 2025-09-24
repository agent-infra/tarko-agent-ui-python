#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""FastAPI example with webui.base configuration for custom routing.

This example demonstrates how to configure the Tarko Agent UI to run
under a custom base path using webui.base configuration.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

try:
    from tarko_agent_ui import get_agent_ui_html
except ImportError:
    print("❌ Error: tarko_agent_ui package not found.")
    print("💡 Install it with: uv add tarko-agent-ui")
    print("💡 Or with pip: pip install tarko-agent-ui")
    exit(1)

app = FastAPI()


@app.get("/")
def home():
    """Serves the Agent UI with custom base path configuration."""
    try:
        return HTMLResponse(
            get_agent_ui_html(
                webui={
                    "base": "/[a-zA-Z0-9]+"
                }
            )
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "suggestion": "Run 'python scripts/build_assets.py' to build static assets"
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail={"error": f"HTML injection failed: {str(e)}"}
        )


@app.get("/{path:path}")
def catch_all(path: str):
    """Catches all other routes and serves the Agent UI."""
    try:
        return HTMLResponse(
            get_agent_ui_html(
                webui={
                    "base": "/[a-zA-Z0-9]+"
                }
            )
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "suggestion": "Run 'python scripts/build_assets.py' to build static assets"
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail={"error": f"HTML injection failed: {str(e)}"}
        )


if __name__ == "__main__":
    print("Starting Tarko Agent UI Server with custom base path")
    print("Available at:")
    print("  - http://localhost:8000/")
    print("  - http://localhost:8000/p9fgsSryzeO5JtefS1bMfsa7G11S6pGKY")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)