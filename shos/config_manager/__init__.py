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
