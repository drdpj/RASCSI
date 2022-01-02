from os import getcwd

REMOVABLE_DEVICE_TYPES = ("SCCD", "SCRM", "SCMO")
CONFIG_FILE_SUFFIX = "json"
DEFAULT_CONFIG = f"default.{CONFIG_FILE_SUFFIX}"

WEB_DIR = getcwd()
HOME_DIR = "/".join(WEB_DIR.split("/")[0:3])
CFG_DIR = f"{HOME_DIR}/.config/rascsi"

RESERVATIONS = ["" for x in range(0, 8)]
