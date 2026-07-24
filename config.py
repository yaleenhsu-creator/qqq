import json
import os

CONFIG_FILE = "config.json"


def load():
    if not os.path.exists(CONFIG_FILE):
        return {
            "x": 300,
            "y": 300,
            "scale": 1.0,
            "affection": 0
        }

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )