from urllib.parse import urlencode
import httpx

from config import API_KEY

# Define the base URL and parameters
base_url = "https://shot.screenshotapi.net/v3/screenshot"
params = {
    "token": API_KEY,
    "width": "800",
    "height": "800",
    "fresh": "false",
    "output": "image",
    "file_type": "png",
    "no_cookie_banners": "true",
    "enable_caching": "true",
    "wait_for_event": "load",
}


async def get_screenshot(input_url: str):
    # Create a copy of params and add the URL
    query_params = params.copy()
    query_params["url"] = f"https://{input_url}/"

    # Construct the full URL
    query_url = f"{base_url}?{urlencode(query_params)}"
    print("query_url", query_url)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(query_url)

        # If the response is a PNG file, return the content
        if response.headers.get("content-type") == "image/png":
            return response.content

        # If the response is a redirect to a PNG file, follow it
        elif response.status_code in (301, 302, 303, 307, 308):
            redirect_url = response.headers.get("location")
            if redirect_url and redirect_url.endswith(".png"):
                redirect_response = await client.get(redirect_url)
                return redirect_response.content

        # If the response is not a PNG file, raise an error
        return response.content
