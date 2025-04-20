from playwright.async_api import async_playwright, Browser, BrowserContext, Page


async def get_screenshot(url: str) -> bytes:
    """
    Take a screenshot of the given URL using Playwright.

    Args:
        url (str): The URL to screenshot

    Returns:
        bytes: The screenshot image data
    """
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch()
        context: BrowserContext = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            permissions=["geolocation"],
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "DNT": "1",
            },
        )
        page: Page = await context.new_page()

        # Block common popup and overlay resources
        await page.route("**/*", lambda route: route.continue_())
        await page.route("**/*.js", lambda route: route.continue_())

        # Block common popup and overlay domains
        await page.route(
            "**/*",
            lambda route: (
                route.continue_()
                if not any(
                    domain in route.request.url
                    for domain in [
                        "consent.",
                        "cookie.",
                        "popup.",
                        "overlay.",
                        "newsletter.",
                        "subscription.",
                        "marketing.",
                        "tracking.",
                    ]
                )
                else route.abort()
            ),
        )

        # Common selectors for overlays and popups
        overlay_selectors = [
            # Cookie consent
            'button[id*="cookie"]',
            'button[id*="consent"]',
            'div[id*="cookie"] button',
            'div[id*="consent"] button',
            'button[class*="cookie"]',
            'button[class*="consent"]',
            # Newsletter popups
            'div[class*="newsletter"]',
            'div[id*="newsletter"]',
            'div[class*="subscribe"]',
            'div[id*="subscribe"]',
            # General overlays
            'div[class*="overlay"]',
            'div[id*="overlay"]',
            'div[class*="modal"]',
            'div[id*="modal"]',
            'div[class*="popup"]',
            'div[id*="popup"]',
            # Close buttons
            'button[class*="close"]',
            'button[id*="close"]',
            'button[aria-label*="close"]',
            'button[class*="dismiss"]',
            'button[id*="dismiss"]',
        ]

        # Try to get rid of overlays and popups
        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            # Try to handle overlays and popups
            for selector in overlay_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        try:
                            # Check if element is visible
                            is_visible = await element.is_visible()
                            if is_visible:
                                # Try to click close buttons
                                if any(
                                    close_word in selector.lower()
                                    for close_word in ["close", "dismiss"]
                                ):
                                    await element.click(timeout=1000)
                                # For other elements, try to remove them
                                else:
                                    await page.evaluate(
                                        "(element) => element.remove()", element
                                    )
                        except:
                            continue
                except:
                    continue

            # Wait for any remaining animations
            await page.wait_for_timeout(1000)

            # Take screenshot of the main content
            screenshot = await page.screenshot()
            return screenshot

        finally:
            await browser.close()
