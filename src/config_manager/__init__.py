import json
from utils.singleton import SingletonMeta


class ConfigManager(metaclass=SingletonMeta):
    _data = None

    def __init__(self, path: str) -> None:
        try:
            f = open(path, "r")
            self._data = json.load(f)
            f.close()
        except FileNotFoundError:
            raise RuntimeError("Unable to find config.json")
        except ValueError:
            raise RuntimeError("Not valid JSON")

    def __getitem__(self, key: str):
        return self._data[key]

    def get_value(self, value: str) -> str:
        temp: str
        temp = self._data[value]
        return temp
