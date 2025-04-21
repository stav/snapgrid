import base64
from pathlib import Path

from starlette.requests import Request
from fasthtml.common import Div, Img

from app.utils import get_valid_url
from .api import capture_screenshot

# Create screenshots directory if it doesn't exist
SCREENSHOTS_DIR = Path("screenshots")
SCREENSHOTS_DIR.mkdir(exist_ok=True)


def filename(url: str) -> str:
    # Generate a filename based on URL
    filename: str = (
        f"{url.replace('https://', '').replace('http://', '').replace('://', '_').replace('/', '_').strip('_')}.png"
    )
    return filename


# Get screenshot from file or capture new one
async def get_or_capture_screenshot(url: str) -> bytes:
    # Check if screenshot already exists
    screenshot_path: Path = SCREENSHOTS_DIR / filename(url)
    if screenshot_path.exists():
        return screenshot_path.read_bytes()

    # Capture new screenshot if not found
    screenshot: bytes = await capture_screenshot(url)
    screenshot_path.write_bytes(screenshot)
    return screenshot


def wrap_snap(url: str, screenshot: bytes):
    # Convert bytes to base64 and create data URL
    base64_image: str = base64.b64encode(screenshot).decode("utf-8")
    data_url: str = f"data:image/png;base64,{base64_image}"

    # Return the screenshot in an img tag with the encoded bytes as the src
    return Div(
        Img(src=data_url, style="width: 100%; height: auto;"),
        cls="brick",
        data_src=data_url,
        data_caption=f"{url} (Saved as: {filename(url)})",
        data_fancybox="gallery",
    )


async def snap_route(request: Request):
    # Validate and format the url from the form data
    form = await request.form()
    url = await get_valid_url(form)
    if url is None:
        return Div("URL is invalid", cls="error")

    # Get screenshot from file or capture new one
    screenshot: bytes = await get_or_capture_screenshot(url)

    # Return the screenshot wrapped for the frontend
    return wrap_snap(url, screenshot)
