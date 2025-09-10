#!/usr/bin/env python3

"""FastAPI example for serving Tarko Agent UI Builder static assets."""

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

try:
    from agent_sandbox import get_static_path
except ImportError:
    print("Error: agent_sandbox package not found. Please install it first:")
    print("cd python && pip install -e .")
    exit(1)


app = FastAPI(
    title="Tarko Agent UI Server",
    description="FastAPI server for serving Tarko Agent UI Builder static assets",
    version="0.1.0"
)


@app.get("/")
async def root():
    """Serve the main index.html file."""
    try:
        static_path = get_static_path()
        index_file = os.path.join(static_path, "index.html")
        
        if not os.path.exists(index_file):
            raise HTTPException(
                status_code=404, 
                detail="index.html not found in static assets"
            )
        
        return FileResponse(index_file)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        static_path = get_static_path()
        return {
            "status": "healthy",
            "static_path": static_path,
            "static_exists": os.path.exists(static_path)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# Mount static files
try:
    static_path = get_static_path()
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    print(f"Mounted static files from: {static_path}")
except FileNotFoundError as e:
    print(f"Warning: {e}")
    print("Static files will not be available until assets are downloaded.")


if __name__ == "__main__":
    uvicorn.run(
        "fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
