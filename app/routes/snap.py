import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from starlette.requests import Request
from fasthtml.common import Div

from app.utils import get_url_filename, lay_brick
from config import SCREENSHOTS_PATH
from .api import capture_screenshot


async def _save_screenshot(url: str, path: Path) -> None:
    screenshot: bytes = await capture_screenshot(url)
    path.write_bytes(screenshot)


def _update_index(url: str, filename: str) -> None:
    """Update the index.json file with new screenshot data."""
    index_data: List[Dict[str, str | int]] = []
    index_path: Path = SCREENSHOTS_PATH / "index.json"
    if index_path.exists():
        index_data = json.loads(index_path.read_text())
    current_time = datetime.now().isoformat()
    snap_data: Dict[str, str | int] = {
        "id": len(index_data) + 1,
        "url": url,
        "filename": filename,
        "datetime": current_time,
    }
    index_data.append(snap_data)
    index_path.write_text(json.dumps(index_data, indent=2))


async def snap_route(request: Request):
    # Validate and format the url from the form data
    form = await request.form()
    url, filename = get_url_filename(form)
    if url is None:
        return Div("URL is invalid", cls="error")

    # Cache new screenshot if one doesn't already exist
    screenshot_path: Path = SCREENSHOTS_PATH / filename
    if not screenshot_path.exists():
        await _save_screenshot(url, screenshot_path)
        _update_index(url, filename)

    # Return an image tag wrapped in a brick
    return lay_brick(url, filename)
