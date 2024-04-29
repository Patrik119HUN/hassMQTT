import json
from typing import Any
from pathlib import Path


def load_config(file_name: str | Path) -> dict[str, Any]:
    try:
        with open(file_name, "r") as jsonfile:
            _data = json.load(jsonfile)
    except FileNotFoundError:
        raise RuntimeError("Unable to find config.json")
    except ValueError:
        raise RuntimeError("Not valid JSON")
    return _data


CONFIG_FILE = (Path(__file__).parent.parent / "../config.json").resolve()

config_manager: dict[str, Any] = load_config(CONFIG_FILE)
