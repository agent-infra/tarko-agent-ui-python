#!/usr/bin/env python3

"""CLI for tarko-web-ui package."""

import argparse
import sys
from pathlib import Path

from . import download_static_assets, get_static_path


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Tarko Web UI CLI",
        prog="tarko-web-ui"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Download command
    download_parser = subparsers.add_parser(
        "download", 
        help="Download static assets from @tarko/agent-ui-builder"
    )
    download_parser.add_argument(
        "--version", 
        type=str, 
        help="Specific version to download (default: latest)"
    )
    
    # Path command
    path_parser = subparsers.add_parser(
        "path", 
        help="Show path to static assets"
    )
    
    # Serve command
    serve_parser = subparsers.add_parser(
        "serve", 
        help="Start FastAPI development server"
    )
    serve_parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to bind to (default: 0.0.0.0)"
    )
    serve_parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind to (default: 8000)"
    )
    serve_parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    if args.command == "download":
        try:
            download_static_assets(version=args.version)
            print("✅ Static assets downloaded successfully")
        except Exception as e:
            print(f"❌ Failed to download static assets: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "path":
        try:
            static_path = get_static_path()
            print(static_path)
        except FileNotFoundError as e:
            print(f"❌ {e}", file=sys.stderr)
            print("💡 Run 'tarko-web-ui download' to download static assets", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "serve":
        try:
            # Import here to avoid circular imports
            import uvicorn
            from .server import create_app
            
            app = create_app()
            uvicorn.run(
                app,
                host=args.host,
                port=args.port,
                reload=args.reload,
                log_level="info"
            )
        except Exception as e:
            print(f"❌ Failed to start server: {e}", file=sys.stderr)
            sys.exit(1)
            
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
