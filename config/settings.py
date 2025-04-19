import configparser
from pathlib import Path
from fasthtml.common import Link, StyleX

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# FastHTML configuration
base_config = {
    "host": "0.0.0.0",
    "port": 8001,
    "debug": True,
    "static_path": str(BASE_DIR / "app"),
    "template_path": str(BASE_DIR / "app"),
    "hdrs": [
        Link(rel="icon", href="/static/favicon.ico"),
        StyleX("app/styles.css"),
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
