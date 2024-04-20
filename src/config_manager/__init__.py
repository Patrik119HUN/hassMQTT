from io import TextIOWrapper
import json
from utils.singleton import SingletonMeta


class _ConfigManager:
    _data = None

    def __init__(self, path: str) -> None:
        _file: TextIOWrapper = None
        try:
            _file = open(path, "r")
            self._data = json.load(_file)
        except FileNotFoundError:
            raise RuntimeError("Unable to find config.json")
        except ValueError:
            raise RuntimeError("Not valid JSON")
        finally:
            _file.close()

    def __getitem__(self, key: str):
        return self._data[key]

    def get_value(self, value: str) -> str:
        temp: str
        temp = self._data[value]
        return temp


config_manager: _ConfigManager = _ConfigManager("../config.json")
