import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from starlette.requests import Request
from fasthtml.common import Div

from app.core import capture_screenshot, SnapResponse
from app.utils import get_url_filename, lay_brick
from config import SCREENSHOTS_PATH


async def _save_screenshot(url: str, path: Path) -> str:
    snap_data: SnapResponse = await capture_screenshot(url)
    path.write_bytes(snap_data["screenshot"])
    return snap_data["title"]


def _update_index(url: str, filename: str, title: str) -> None:
    """Update the index.json file with new screenshot data."""
    index_data: List[Dict[str, str | int]] = []
    index_path: Path = SCREENSHOTS_PATH / "index.json"
    if index_path.exists():
        index_data = json.loads(index_path.read_text())

    # Check if snap with same URL exists
    existing_snap = next((item for item in index_data if item["url"] == url), None)

    if existing_snap:
        # Update existing snap data while preserving ID
        existing_snap.update(
            {
                "filename": filename,
                "datetime": datetime.now().isoformat(),
            }
        )
    else:
        # Add new snap data with new ID
        snap_data: Dict[str, str | int] = {
            "id": len(index_data) + 1,
            "url": url,
            "title": title,
            "filename": filename,
            "datetime": datetime.now().isoformat(),
        }
        index_data.append(snap_data)

    index_path.write_text(json.dumps(index_data, indent=2))


async def snap_route(request: Request):
    # Validate and format the url from the form data
    form = await request.form()
    url, filename = get_url_filename(form)
    if url is None:
        return Div("URL is invalid", cls="error")

    # Cache new screenshot
    title = await _save_screenshot(url, SCREENSHOTS_PATH / filename)

    # Update the index.json file
    _update_index(url, filename, title)

    # Return an image tag wrapped in a brick
    return lay_brick(url, filename)
