from typing import TypedDict

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config.settings import get_login_credentials


# Common selectors for overlays and popups
OVERLAY_SELECTORS = [
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

# Domains to block for popups and overlays
BLOCKED_DOMAINS = [
    "consent.",
    "cookie.",
    "popup.",
    "overlay.",
    "newsletter.",
    "subscription.",
    "marketing.",
    "tracking.",
]

# Browser context configuration
BROWSER_CONTEXT_CONFIG = {
    "viewport": {"width": 1920, "height": 1080},
    "permissions": ["geolocation"],
    "extra_http_headers": {
        "Accept-Language": "en-US,en;q=0.9",
        "DNT": "1",
    },
}

# Login form selectors
LOGIN_SELECTORS = [
    'form[class*="login"]',
    'form[id*="login"]',
    'div[class*="login-box"]',
    'div[id*="login-box"]',
    'div[class*="login-form"]',
    'div[id*="login-form"]',
]


class SnapResponse(TypedDict):
    screenshot: bytes
    title: str


async def capture_screenshot(url: str) -> SnapResponse:
    """
    Take a screenshot of the given URL using Playwright.

    Args:
        url (str): The URL to screenshot

    Returns:
        dict[str, bytes]: A dictionary containing the screenshot image data
    """
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(headless=True)
        context: BrowserContext = await browser.new_context(**BROWSER_CONTEXT_CONFIG)
        page: Page = await context.new_page()

        # Block common popup and overlay resources
        await page.route("**/*", lambda route: route.continue_())
        await page.route("**/*.js", lambda route: route.continue_())

        # Block common popup and overlay domains
        await page.route(
            "**/*",
            lambda route: (
                route.continue_()
                if not any(domain in route.request.url for domain in BLOCKED_DOMAINS)
                else route.abort()
            ),
        )

        try:
            await page.goto(url)
            try:
                await page.wait_for_load_state("networkidle")
            except TimeoutError:
                # If network doesn't become idle, continue anyway
                pass

            # Get credentials for this domain if available
            credentials = get_login_credentials(url)
            print("credentials", credentials)
            
            # Check for login form and attempt to login if found and credentials are available
            if credentials:
                for selector in LOGIN_SELECTORS:
                    print("credentials selector", selector)
                    login_form = await page.query_selector(selector)
                    if login_form:
                        print("login_form", login_form)
                        # Try to find email and password fields
                        email_field = await page.query_selector('input[type="email"], input[name*="email"], input[id*="email"]')
                        password_field = await page.query_selector('input[type="password"], input[name*="password"], input[id*="password"]')
                        print("email_field", email_field)
                        print("password_field", password_field)

                        if email_field and password_field:
                            # Fill in credentials
                            await email_field.fill(credentials["email"])
                            await password_field.fill(credentials["password"])
                            
                            # Try to find and click submit button
                            submit_button = await page.query_selector('button[type="submit"], input[type="submit"], button[class*="submit"], button[id*="submit"]')
                            print("submit_button", submit_button)
                            if submit_button:
                                await submit_button.click()
                                # Wait for navigation after login
                                try:
                                    await page.wait_for_load_state("networkidle", timeout=20000)
                                except TimeoutError:
                                    # If network doesn't become idle after login, continue anyway
                                    pass
                                await page.wait_for_timeout(2000)  # Wait for any post-login redirects
                                break

            # Try to handle overlays and popups
            for selector in OVERLAY_SELECTORS:
                print("overlay selector", selector)
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
            print("waiting for timeout")
            await page.wait_for_timeout(1000)
            # Take screenshot of the main content
            screenshot: bytes = await page.screenshot()
            # Try to get OpenGraph title if available
            title = await page.title()
            try:
                og_title = await page.evaluate(
                    """() => document.querySelector('meta[property="og:title"]')?.content"""
                )
                if og_title:
                    title = og_title
            except:
                pass
            return {"screenshot": screenshot, "title": title}

        finally:
            await browser.close()
