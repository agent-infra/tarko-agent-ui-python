#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Complete FastAPI example using tarko_web_ui SDK.

This example demonstrates how to integrate the tarko_web_ui SDK
with a FastAPI application to serve the Tarko Agent UI.
"""

import os
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

try:
    from tarko_web_ui import get_static_path, get_static_version
except ImportError:
    print("❌ Error: tarko_web_ui package not found.")
    print("💡 Install it with: uv add tarko-web-ui")
    print("💡 Or with pip: pip install tarko-web-ui")
    exit(1)


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Tarko Agent UI Server",
        description="FastAPI server for serving Tarko Agent UI Builder static assets",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
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
                    detail={
                        "error": "index.html not found in static assets",
                        "suggestion": "Run 'python scripts/build_assets.py' to build static assets"
                    }
                )
            
            return FileResponse(str(index_file))
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=500, 
                detail={
                    "error": str(e),
                    "suggestion": "Run 'python scripts/build_assets.py' to build static assets"
                }
            )
    
    @app.get("/api/health")
    async def health_check():
        """Health check endpoint with detailed status."""
        try:
            static_path = get_static_path()
            static_path_obj = Path(static_path)
            index_exists = (static_path_obj / "index.html").exists()
            version_info = get_static_version()
            
            # Count static files
            all_files = list(static_path_obj.rglob("*")) if static_path_obj.exists() else []
            file_count = len([f for f in all_files if f.is_file()])
            
            return {
                "status": "healthy" if index_exists else "degraded",
                "static_path": static_path,
                "static_exists": static_path_obj.exists(),
                "index_exists": index_exists,
                "file_count": file_count,
                "assets_version": version_info["version"],
                "assets_package": version_info["package"],
                "sdk_version": version_info["sdk_version"]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "suggestion": "Run 'python scripts/build_assets.py' to build static assets"
            }
    
    @app.get("/api/version")
    async def version_info():
        """Get version information about static assets."""
        try:
            return get_static_version()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Failed to get version info: {e}",
                    "suggestion": "Run 'python scripts/build_assets.py' to build static assets"
                }
            )
    
    # Mount static files if available
    try:
        static_path = get_static_path()
        app.mount("/static", StaticFiles(directory=static_path), name="static")
        version_info = get_static_version()
        print(f"✅ Mounted static files from: {static_path}")
        print(f"📦 Assets version: {version_info['package']}@{version_info['version']}")
    except FileNotFoundError as e:
        print(f"⚠️  {e}")
        print("💡 Run 'python scripts/build_assets.py' to build static assets")
    
    return app


def main():
    """Main entry point for running the server."""
    print("🚀 Starting Tarko Agent UI Server...")
    print("📱 Open http://localhost:8000 in your browser")
    print("🔍 Health check: http://localhost:8000/api/health")
    print("📚 API docs: http://localhost:8000/api/docs")
    print("🏷️  Version info: http://localhost:8000/api/version")
    print("")
    
    # Check if static assets exist
    try:
        get_static_path()
        version_info = get_static_version()
        print(f"✅ Static assets found: {version_info['package']}@{version_info['version']}")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("💡 Run 'python scripts/build_assets.py' to build static assets")
        print("   Server will start but static routes will be unavailable.")
    
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
