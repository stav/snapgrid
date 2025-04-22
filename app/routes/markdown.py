from pathlib import Path
from starlette.requests import Request
from fasthtml.common import Div, Form, Textarea, Button

from config import SCREENSHOTS_PATH


async def markdown_route(request: Request):
    # Get the filename from the URL path parameter
    filename = request.path_params["filename"]
    # Strip .png extension if present
    if filename.endswith(".png"):
        filename = filename[:-4]
    print(f"filename: {filename}")

    # Load the markdown content from the file
    markdown_path = SCREENSHOTS_PATH / f"{filename}.md"
    content = ""
    if markdown_path.exists():
        content = markdown_path.read_text()

    # Return the markdown content in an editable form
    return Div(
        Form(
            Textarea(
                name="content", 
                value=content,
                style="width: 100%; min-height: 200px; margin-bottom: 8px;",
            ),
            Button("Save Changes", type="submit", style="padding: 4px 12px;"),
            hx_post=f"/markdown/{filename}/",
        )
    )
