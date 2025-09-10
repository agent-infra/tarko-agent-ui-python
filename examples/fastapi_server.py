#!/usr/bin/env python3

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
    from tarko_web_ui import get_static_path, download_static_assets
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
                        "suggestion": "Run: python -c 'from tarko_web_ui import download_static_assets; download_static_assets()'"
                    }
                )
            
            return FileResponse(str(index_file))
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=500, 
                detail={
                    "error": str(e),
                    "suggestion": "Run: python -c 'from tarko_web_ui import download_static_assets; download_static_assets()'"
                }
            )
    
    @app.get("/api/health")
    async def health_check():
        """Health check endpoint with detailed status."""
        try:
            static_path = get_static_path()
            static_path_obj = Path(static_path)
            index_exists = (static_path_obj / "index.html").exists()
            
            # Count static files
            file_count = len(list(static_path_obj.rglob("*"))) if static_path_obj.exists() else 0
            
            return {
                "status": "healthy" if index_exists else "degraded",
                "static_path": static_path,
                "static_exists": static_path_obj.exists(),
                "index_exists": index_exists,
                "file_count": file_count,
                "version": "0.1.0"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "suggestion": "Run: python -c 'from tarko_web_ui import download_static_assets; download_static_assets()'"
            }
    
    @app.post("/api/download-assets")
    async def download_assets(version: Optional[str] = None):
        """Download static assets endpoint."""
        try:
            download_static_assets(version=version)
            return {
                "status": "success",
                "message": f"Downloaded assets{f' version {version}' if version else ''}"
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Failed to download assets: {e}",
                    "suggestion": "Check internet connection and npm registry availability"
                }
            )
    
    # Mount static files if available
    try:
        static_path = get_static_path()
        app.mount("/static", StaticFiles(directory=static_path), name="static")
        print(f"✅ Mounted static files from: {static_path}")
    except FileNotFoundError:
        print("⚠️  Static assets not found.")
        print("💡 Download them with: python -c 'from tarko_web_ui import download_static_assets; download_static_assets()'")
        print("   Or use the API endpoint: POST /api/download-assets")
    
    return app


def main():
    """Main entry point for running the server."""
    print("🚀 Starting Tarko Agent UI Server...")
    print("📱 Open http://localhost:8000 in your browser")
    print("🔍 Health check: http://localhost:8000/api/health")
    print("📚 API docs: http://localhost:8000/api/docs")
    print("")
    
    # Check if static assets exist, if not, try to download them
    try:
        get_static_path()
        print("✅ Static assets found")
    except FileNotFoundError:
        print("⚠️  Static assets not found, attempting to download...")
        try:
            download_static_assets()
            print("✅ Static assets downloaded successfully")
        except Exception as e:
            print(f"❌ Failed to download static assets: {e}")
            print("💡 You can download them later using: POST /api/download-assets")
    
    # Create and run the app
    app = create_app()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
