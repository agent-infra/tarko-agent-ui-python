#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Complete FastAPI example using tarko_agent_ui SDK.

This example demonstrates how to integrate the tarko_agent_ui SDK
with a FastAPI application to serve the Tarko Agent UI.
"""

from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

try:
    from tarko_agent_ui import get_static_path, get_static_version
except ImportError:
    print("❌ Error: tarko_agent_ui package not found.")
    print("💡 Install it with: uv add tarko-agent-ui")
    print("💡 Or with pip: pip install tarko-agent-ui")
    exit(1)


def handle_missing_assets(e: FileNotFoundError, context: str = "api") -> None:
    """Handles FileNotFoundError with context-appropriate responses."""
    suggestion = "Run 'python scripts/build_assets.py' to build static assets"
    
    if context == "api":
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "suggestion": suggestion
            }
        )
    else:
        print(f"❌ {e}")
        print(f"💡 {suggestion}")


def create_app() -> FastAPI:
    """Creates FastAPI app with static asset routing and health endpoints."""
    app = FastAPI(
        title="Tarko Agent UI Server",
        description="FastAPI server for serving Tarko Agent UI Builder static assets",
        version="0.1.0"
    )
    
    @app.get("/")
    async def root():
        """Serves the main UI application."""
        try:
            static_path = get_static_path()
            index_file = Path(static_path) / "index.html"
            
            if not index_file.exists():
                handle_missing_assets(
                    FileNotFoundError("index.html not found in static assets"), 
                    "api"
                )
            
            return FileResponse(str(index_file))
        except FileNotFoundError as e:
            handle_missing_assets(e, "api")
    
    @app.get("/api/v1/health")
    async def health_check():
        """Returns server status for monitoring."""
        return {"status": "ok"}
    
    # Mount static files if available
    try:
        static_path = get_static_path()
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    except FileNotFoundError as e:
        handle_missing_assets(e, "startup")
    
    return app


def main():
    """Starts the development server with asset validation."""
    print("Starting Tarko Agent UI Server on http://localhost:8000")
    
    # Check if static assets exist
    try:
        get_static_path()
        version_info = get_static_version()
        print(f"Assets: {version_info['package']}@{version_info['version']}")
    except FileNotFoundError as e:
        handle_missing_assets(e, "startup")
        print("Warning: Static routes will be unavailable")
    
    # Create and run the app
    app = create_app()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
