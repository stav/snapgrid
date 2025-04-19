import base64

from starlette.requests import Request
from fasthtml.common import Div, Img

from .api import get_screenshot


async def fetch_route(request: Request):
    form = await request.form()
    url = form.get("url")
    if not url or not isinstance(url, str):
        return "Please enter a valid URL"

    # Get the screenshot of the URL
    screenshot = await get_screenshot(url)

    # Convert bytes to base64 and create data URL
    base64_image = base64.b64encode(screenshot).decode("utf-8")
    data_url = f"data:image/png;base64,{base64_image}"

    return Div(
        Img(src=data_url),
        cls="brick",
    )
