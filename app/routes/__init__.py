import base64

from starlette.requests import Request
from fasthtml.common import Button, Div, Form, Input, Span, Style, Titled, Img
from fasthtml.svg import Circle, Svg


from .api import get_screenshot


def router(rt):

    # Define routes
    @rt("/")
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
                    Button(
                        "Snap",
                        Span(
                            Svg(
                                Circle(
                                    cx="25",
                                    cy="25",
                                    r="20",
                                    fill="none",
                                    stroke_width="5",
                                    cls="path",
                                ),
                                cls="spinner-svg",
                                viewBox="0 0 50 50",
                            ),
                            id="spinner",
                            cls="spinner",
                        ),
                        type="submit",
                        style="position: relative; padding: 8px 16px;",
                        hx_post="/fetch-url",
                        hx_swap="innerHTML",
                        hx_target="#result",
                        hx_indicator="#spinner",
                        hx_on__before_request="this.disabled = true; document.getElementById('result').innerHTML = ''",
                        hx_on__after_request="this.disabled = false",
                    ),
                    Div(id="result"),
                ),
                Style(
                    """
                    .spinner {
                        visibility: hidden;
                        display: inline-block;
                        position: absolute;
                        top: 20%;
                        right: 30%;
                    }

                    .spinner.htmx-request  {
                        visibility: visible;
                    }

                    .spinner-svg {
                        animation: rotate 2s linear infinite;
                        width: 20px;
                        height: 20px;
                    }

                    .path {
                        stroke: white;
                        stroke-linecap: round;
                        animation: dash 1.5s ease-in-out infinite;
                    }

                    @keyframes rotate {
                        100% { transform: rotate(360deg); }
                    }

                    @keyframes dash {
                        0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
                        50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
                        100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
                    }
                    """
                ),
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
