#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Complete FastAPI example using tarko_agent_ui SDK.

This example demonstrates how to integrate the tarko_agent_ui SDK
with a FastAPI application to serve the Tarko Agent UI.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

try:
    from tarko_agent_ui import get_agent_ui_html, get_static_path, get_static_version
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
            status_code=500, detail={"error": str(e), "suggestion": suggestion}
        )
    else:
        print(f"❌ {e}")
        print(f"💡 {suggestion}")


def create_app(
    base_url: str = "", ui_config: Optional[Dict[str, Any]] = None
) -> FastAPI:
    """Creates FastAPI app with static asset routing and health endpoints.

    Args:
        base_url: Agent API base URL for environment injection
        ui_config: UI configuration object for environment injection
    """
    app = FastAPI(
        title="Tarko Agent UI Server",
        description="FastAPI server for serving Tarko Agent UI Builder static assets",
        version="0.1.0",
    )

    @app.get("/", response_class=HTMLResponse)
    async def root() -> HTMLResponse:
        """Serves the main UI application with injected environment variables."""
        try:
            html_content = get_agent_ui_html(base_url=base_url, ui_config=ui_config)
            return HTMLResponse(content=html_content)
        except FileNotFoundError as e:
            handle_missing_assets(e, "api")
            # This line is unreachable but satisfies mypy
            raise  # pragma: no cover
        except ValueError as e:
            raise HTTPException(
                status_code=500, detail={"error": f"HTML injection failed: {str(e)}"}
            )

    @app.get("/api/v1/health")
    async def health_check() -> Dict[str, str]:
        """Returns server status for monitoring."""
        return {"status": "ok"}

    # Mount static files if available
    try:
        static_path = get_static_path()
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    except FileNotFoundError as e:
        handle_missing_assets(e, "startup")

    return app


def main() -> None:
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

    # Get base URL from environment variable or use default
    base_url = os.getenv("AGENT_BASE_URL", "http://localhost:8000/api")

    print(f"Agent Base URL: {base_url}")

    # Omni Agent UI configuration
    ui_config = {
        "logo": "https://lf3-static.bytednsdoc.com/obj/eden-cn/zyha-aulnh/ljhwZthlaukjlkulzlp/icon.png",
        "title": "Omni Agent",
        "subtitle": "Offering seamless integration with a wide range of real-world tools.",
        "welcomTitle": "A multimodal AI agent",
        "welcomePrompts": [
            "Search for the latest GUI Agent papers",
            "Find information about UI TARS",
            "Tell me the top 5 most popular projects on ProductHunt today",
            "Write hello world using python",
            "Use jupyter to calculate which is greater in 9.11 and 9.9",
            "Write code to reproduce seed-tars.com",
            "Summary seed-tars.com/1.5",
            "Write a python code to download the paper https://arxiv.org/abs/2505.12370, and convert the pdf to markdown",
            "Search news about bytedance seed1.6 model, then write a web page in modern style and deploy it",
            "Write a minimal code sample to help me use transformer",
            "Please search for trending datasets on Hugging Face, download the top-ranked dataset, and calculate the total number of characters in the entire datase.",
            "Identify the independence process of a twin-island nation where the pro-self-governance political group won thirteen out of seventeen legislative seats in spring 1980 national polls, a second constitutional conference was held at a historic London venue in late 1980, liberation from colonial rule is annually commemorated on November 1st as a public holiday, and an agreement revised the smaller island's local governance legislation for enhanced autonomy. What was the composition of the associated state that preceded its independence?",
            "I am a high school music theory teacher and i'm preparing a course on basic music theory to explain knowledge about music names, roll titles, major scales, octave distribution, and physical frequency. Please help me collect enough informations, design fulfilling and authoritative course content with demonstration animations, and finally output them as web page",
        ],
        "workspace": {
            "navItems": [
                {
                    "title": "Github",
                    "link": "https://github.com/agent-infra/tarko-agent-ui-python",
                    "icon": "code",
                }
            ]
        },
        "guiAgent": {
            "defaultScreenshotRenderStrategy": "afterAction",
            "enableScreenshotRenderStrategySwitch": True,
            "renderGUIAction": True,
            "renderBrowserShell": False,
        },
        "layout": {"enableLayoutSwitchButton": True},
    }

    app = create_app(base_url=base_url, ui_config=ui_config)

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")


if __name__ == "__main__":
    main()
