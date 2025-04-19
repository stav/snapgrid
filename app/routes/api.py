import asyncio
from playwright.async_api import async_playwright


async def get_screenshot(url: str) -> bytes:
    """
    Take a screenshot of the given URL using Playwright.

    Args:
        url (str): The URL to screenshot

    Returns:
        bytes: The screenshot image data
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            screenshot = await page.screenshot()
            return screenshot
        finally:
            await browser.close()
