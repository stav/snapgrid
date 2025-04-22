from fasthtml.common import Div, Img

from config.settings import SCREENSHOT_DIR


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
