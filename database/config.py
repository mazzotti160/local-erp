import os
import json

_CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "LK-ERP")
_CONFIG_FILE = os.path.join(_CONFIG_DIR, "config.json")


def get_db_path():
    if not os.path.exists(_CONFIG_FILE):
        return None
    try:
        with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("db_path")
    except Exception:
        return None


def set_db_path(path: str):
    os.makedirs(_CONFIG_DIR, exist_ok=True)
    with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"db_path": path}, f, indent=2)
