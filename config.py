import os
import configparser

base_config = {}

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

file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(file_path)
mixed_path = os.path.join(parent_dir, "config.ini")
config_path = os.path.abspath(mixed_path)
config = configparser.ConfigParser()
config.read(config_path)

API_KEY = config["SCREENSHOTAPI.NET"]["API_KEY"]
