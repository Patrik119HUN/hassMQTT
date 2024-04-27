import json
from typing import Any


def load_config(file_name: str) -> dict[str, Any]:
    try:
        with open(file_name, "r") as jsonfile:
            _data = json.load(jsonfile)
    except FileNotFoundError:
        raise RuntimeError("Unable to find config.json")
    except ValueError:
        raise RuntimeError("Not valid JSON")
    return _data


config_manager: dict[str, Any] = load_config('C:\\Users\\patri\\PycharmProjects\\hassMQTT\\config.json')
