"""
    app worker
"""

import os
from datetime import datetime
import uvicorn  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import FastAPI

from fastapi_template_project.version import VERSION

STARTUP_DATETIME = datetime.now()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def app_description() -> str:
    """Get the app description."""
    lines = []
    lines.append("# fastapi_template_project")
    lines.append("  * Version: " + VERSION)
    lines.append("  * Started at: " + str(STARTUP_DATETIME))
    return "\n".join(lines)


app = FastAPI(
    title="Video Server",
    version=VERSION,
    redoc_url=None,
    license_info={
        "name": "Private program, do not distribute",
    },
    description=app_description(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    """By default redirect to the fastapi docs."""
    return RedirectResponse(url="/docs", status_code=302)


@app.get("/get")
async def log_file() -> JSONResponse:
    """TODO - Add description."""
    return JSONResponse({"hello": "world"})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
