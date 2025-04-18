from starlette.requests import Request
from fasthtml.common import *

dev_config = {
    "live": True,
    "debug": True,
}

app, rt = fast_app(**dev_config)
serve()


@rt
def index():
    return Titled("SnapGrid", 
        Div(
            Form(
                Input(type="text", name="url", required=True, placeholder="Enter URL", style="padding: 8px"),
                Button("Snap", type="submit"),
                Div(id="result", style="margin-top: 20px;"),
                hx_post="/fetch-url",
                hx_target="#result",
            )
        )
    )

@rt("/fetch-url")
async def _(request: Request):
    form = await request.form()
    url = form.get('url')
    if not url:
        return "Please enter a URL"
    return f"Fetching URL: {url}"
