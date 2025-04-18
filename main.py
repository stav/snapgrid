import base64
from starlette.requests import Request
from fasthtml.common import *

from config import fast_config
from app import get_screenshot

# Create the FastHTML app
app, rt = fast_app(**fast_config)


# Define routes
@rt
def index():
    return Titled(
        "SnapGrid",
        Div(
            Form(
                Input(
                    type="text",
                    name="url",
                    required=True,
                    placeholder="Enter URL",
                    style="padding: 8px",
                ),
                Button("Snap", type="submit"),
                Div(id="result"),
                hx_post="/fetch-url",
                hx_target="#result",
            )
        ),
    )


@rt("/fetch-url")
async def _(request: Request):
    form = await request.form()
    url = form.get("url")
    if not url:
        return "Please enter a URL"

    # Get the screenshot of the URL
    screenshot = await get_screenshot(url)

    # Convert bytes to base64 and create data URL
    base64_image = base64.b64encode(screenshot).decode("utf-8")
    data_url = f"data:image/png;base64,{base64_image}"

    return Img(src=data_url)


# Only run the server if this file is executed directly
if __name__ == "__main__":
    serve()
