from fasthtml.common import Div, Img
import json

from config import SCREENSHOT_DIR, SCREENSHOTS_PATH


def get_url_filename(form) -> tuple[str | None, str]:
    url = form.get("url")
    if not url or not isinstance(url, str):
        return None, ""

    # Split URL on spaces and use first part as URL, rest as filename
    url, filename = f"{url} ".split(" ", 1)
    url = url.strip()
    filename = filename.strip()
    if not filename:
        filename: str = (
            url.replace("https://", "")
            .replace("http://", "")
            .replace("://", "_")
            .replace("/", "_")
            .strip("_")
        )

    # Ensure URL starts with http:// or https://
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    return url, f"{filename}.png"


def lay_brick(url, filename):
    return Div(
        Img(
            src=f"/static/{SCREENSHOT_DIR}/{filename}",
            style="width: 100%; height: auto;",
            alt=f"Screenshot of {url}",
        ),
        cls="brick",
        title=f"{url} (Saved as: {filename})",
        data_src=f"/static/{SCREENSHOT_DIR}/{filename}",
        data_caption=f"{url} (Saved as: {filename})",
        data_fancybox="gallery",
    )


def get_index_file():
    return SCREENSHOTS_PATH / "index.json"


def get_index_data():
    """Collect and sort index data from index file."""
    SCREENSHOTS_PATH.mkdir(parents=True, exist_ok=True)
    index_file = get_index_file()
    if not index_file.exists():
        # Create empty index.json with an empty list
        index_file.write_text("[]", encoding="utf-8")
        return []

    index_data = json.loads(index_file.read_text(encoding="utf-8"))
    return sorted(index_data, key=lambda x: x["id"])
