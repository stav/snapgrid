import json
from datetime import datetime
from pathlib import Path

from starlette.requests import Request
from fasthtml.common import Div, Img

from app.utils import get_valid_url
from config import SCREENSHOTS_PATH, SCREENSHOT_DIR
from .api import capture_screenshot


def get_filename(url: str) -> str:
    # Generate a filename based on URL
    filename: str = (
        url.replace("https://", "")
        .replace("http://", "")
        .replace("://", "_")
        .replace("/", "_")
        .strip("_")
    )
    return f"{filename}.png"


async def snap_route(request: Request):
    # Validate and format the url from the form data
    form = await request.form()
    url = await get_valid_url(form)
    if url is None:
        return Div("URL is invalid", cls="error")

    # Cache new screenshot if one doesn't already exist
    filename: str = get_filename(url)
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
    request_pathname: str = f"/static/{SCREENSHOT_DIR}/{filename}"
    return Div(
        Img(src=request_pathname, style="width: 100%; height: auto;"),
        cls="brick",
        data_src=request_pathname,
        data_caption=f"{url} (Saved as: {filename})",
        data_fancybox="gallery",
    )
