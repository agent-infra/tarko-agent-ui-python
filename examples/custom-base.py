from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from tarko_agent_ui import get_agent_ui_html
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return HTMLResponse(get_agent_ui_html(webui={"base": "/[a-zA-Z0-9]+"}))


@app.get("/{path:path}")
def catch_all(path: str):
    return HTMLResponse(get_agent_ui_html(webui={"base": "/[a-zA-Z0-9]+"}))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)