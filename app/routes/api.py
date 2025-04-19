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
        context = await browser.new_context(
            # Block popups and notifications
            viewport={'width': 1920, 'height': 1080},
            permissions=['geolocation'],
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9',
                'DNT': '1',
            }
        )
        page = await context.new_page()

        # Block common popup selectors
        await page.route('**/*', lambda route: route.continue_())
        
        # Add common cookie consent selectors to click
        cookie_selectors = [
            'button[id*="cookie"]',
            'button[id*="consent"]',
            'div[id*="cookie"] button',
            'div[id*="consent"] button',
            'button[class*="cookie"]',
            'button[class*="consent"]',
        ]

        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            
            # Try to handle cookie consent dialogs
            for selector in cookie_selectors:
                try:
                    await page.click(selector, timeout=1000)
                except:
                    continue
            
            # Wait a bit for any animations to complete
            await page.wait_for_timeout(1000)
            
            screenshot = await page.screenshot()
            return screenshot
        finally:
            await browser.close()
