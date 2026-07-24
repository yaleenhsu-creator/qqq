import json
import os

CONFIG_FILE = "config.json"

DEFAULT = {
    "x": 200,
    "y": 200,
    "scale": 1.0,
    "always_on_top": True
}


def load():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for k, v in DEFAULT.items():
            if k not in data:
                data[k] = v

        return data

    except:
        return DEFAULT.copy()


def save(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)