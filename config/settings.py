import configparser
from pathlib import Path
from fasthtml.common import Link, StyleX, Script, ScriptX

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent
# Create screenshots directory if it doesn't exist
SCREENSHOT_DIR = "screenshots"
SCREENSHOTS_PATH = Path("app", "static", SCREENSHOT_DIR)
SCREENSHOTS_PATH.mkdir(parents=True, exist_ok=True)

# FastHTML configuration
base_config = {
    "host": "0.0.0.0",
    "debug": True,
    "static_path": str(BASE_DIR / "app"),
    "template_path": str(BASE_DIR / "app"),
    "hdrs": [
        Link(rel="icon", href="/static/favicon.ico"),
        StyleX("app/styles.css"),
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css",
        ),
        Script(
            src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js",
        ),
        ScriptX("app/fancybox.js"),
        Script("//htmx.logAll();"),
    ],
}

dev_config = {
    "live": True,
    "debug": True,
    **base_config,
}

prod_config = {
    "live": False,
    "debug": False,
    **base_config,
}

fast_config = dev_config

# Read config file
config_path = BASE_DIR / "config" / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)

# Export config variables
API_KEY = config["SCREENSHOTAPI.NET"]["API_KEY"]
