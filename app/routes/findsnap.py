import base64

from starlette.requests import Request
from fasthtml.common import Div, Img

from .api import capture_screenshot


async def findsnap_route(request: Request):
    # Get the url from the form data
    form = await request.form()
    url = form.get("url")
    if not url or not isinstance(url, str):
        return "Please enter a valid URL"

    # Get the screenshot of the URL
    screenshot: bytes = await capture_screenshot(url)

    # Convert bytes to base64 and create data URL
    base64_image: str = base64.b64encode(screenshot).decode("utf-8")
    data_url: str = f"data:image/png;base64,{base64_image}"

    # Return the screenshot in an img tag with the encoded bytes as the src
    return Div(
        Img(src=data_url, style="width: 100%; height: auto;"),
        cls="brick",
        data_src=data_url,
        data_caption=url,
        data_fancybox="gallery",
    )
