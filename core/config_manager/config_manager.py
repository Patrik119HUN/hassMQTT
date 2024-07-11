import json
from typing import Any
from pathlib import Path
from dotenv import dotenv_values
from loguru import logger


class ConfigManager:
    def __init__(self, file_name: str | Path = None):
        logger.trace("ConfigManager initialized")
        self.__config = self.load_config(file_name)

    def __getitem__(self, item):
        return self.__config[item]

    def load_env(self, name: str, file_name: str | Path = None):
        values = {k.lower(): v for k, v in dotenv_values(file_name).items()}
        self.__config[name].update(values)

    def load_config(self, file_name: str | Path = None) -> dict[str, Any]:
        """
        Reads a JSON file named `config.json`. It parses the content of the file using
        `json.load()` and returns the parsed data.

        Args:
            file_name (str | Path): name of a file to be read from, which is then
                opened using the `open()` method to retrieve its JSON content.

        Returns:
            dict[str, Any]: a JSON-formatted dictionary containing configuration data.

        """
        try:
            with open(file_name, "r") as jsonfile:
                logger.debug(f"Loading {file_name}")
                _data = json.load(jsonfile)
        except FileNotFoundError:
            raise RuntimeError(f"Unable to find {file_name}")
        except ValueError:
            raise RuntimeError("Not valid JSON")
        return _data
