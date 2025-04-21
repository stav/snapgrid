async def get_valid_url(form) -> str | None:
    url = form.get("url")
    if not url or not isinstance(url, str):
        return None

    # Ensure URL starts with http:// or https://
    if url.startswith(("http://", "https://")):
        return url

    return f"https://{url}"
