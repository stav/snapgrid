import json
from datetime import datetime
from pathlib import Path

from starlette.requests import Request
from fasthtml.common import Div

from app.utils import get_url_filename, lay_brick
from config import SCREENSHOTS_PATH
from .api import capture_screenshot


async def snap_route(request: Request):
    # Validate and format the url from the form data
    form = await request.form()
    url, filename = get_url_filename(form)
    if url is None:
        return Div("URL is invalid", cls="error")

    # Cache new screenshot if one doesn't already exist
    screenshot_path: Path = SCREENSHOTS_PATH / filename
    if not screenshot_path.exists():
        # Capture the screenshot
        screenshot: bytes = await capture_screenshot(url)
        screenshot_path.write_bytes(screenshot)
        # Update the index
        index_path: Path = SCREENSHOTS_PATH / "index.json"
        if index_path.exists():
            index_data = json.loads(index_path.read_text())
        else:
            index_data = {}
        current_time = datetime.now().isoformat()
        index_data[filename] = {"url": url, "datetime": current_time}
        index_data = dict(sorted(index_data.items()))
        index_path.write_text(json.dumps(index_data, indent=2))

    # Return an image tag wrapped in a brick
    return lay_brick(url, filename)
