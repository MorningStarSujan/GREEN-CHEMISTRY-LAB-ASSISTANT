import json
import os
from datetime import datetime


def load_json(filename):
    filepath = os.path.join("data", filename)

    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except:
        return []


def save_json(filename, data):
    filepath = os.path.join("data", filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def add_history(module, activity):
    # Vercel does not support persistent local file writes.
    return


def get_history():
    return load_json("history.json")


def clear_history():
    # Vercel does not support persistent local file writes.
    return
