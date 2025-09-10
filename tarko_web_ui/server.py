#!/usr/bin/env python3

"""FastAPI server for serving Tarko Agent UI Builder static assets."""

import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from . import get_static_path


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Tarko Web UI Server",
        description="FastAPI server for serving Tarko Agent UI Builder static assets",
        version="0.1.0"
    )
    
    @app.get("/")
    async def root():
        """Serve the main index.html file."""
        try:
            static_path = get_static_path()
            index_file = Path(static_path) / "index.html"
            
            if not index_file.exists():
                raise HTTPException(
                    status_code=404, 
                    detail="index.html not found in static assets. Run 'tarko-web-ui download' to download assets."
                )
            
            return FileResponse(str(index_file))
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=500, 
                detail=f"{e}. Run 'tarko-web-ui download' to download assets."
            )
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        try:
            static_path = get_static_path()
            static_path_obj = Path(static_path)
            return {
                "status": "healthy",
                "static_path": static_path,
                "static_exists": static_path_obj.exists(),
                "index_exists": (static_path_obj / "index.html").exists()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "suggestion": "Run 'tarko-web-ui download' to download static assets"
            }
    
    # Mount static files if available
    try:
        static_path = get_static_path()
        app.mount("/static", StaticFiles(directory=static_path), name="static")
        print(f"✅ Mounted static files from: {static_path}")
    except FileNotFoundError:
        print("⚠️  Static assets not found. Run 'tarko-web-ui download' to download them.")
        print("   Static file serving will be unavailable until assets are downloaded.")
    
    return app
