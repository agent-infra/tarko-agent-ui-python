#!/usr/bin/env python3

"""Simple FastAPI example using tarko_web_ui."""

import uvicorn
from tarko_web_ui.server import create_app


if __name__ == "__main__":
    # Create the FastAPI app
    app = create_app()
    
    # Run the server
    print("🚀 Starting Tarko Web UI server...")
    print("📱 Open http://localhost:8000 in your browser")
    print("🔍 Health check: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
