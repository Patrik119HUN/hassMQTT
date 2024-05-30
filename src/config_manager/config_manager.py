import json
from typing import Any

from pathlib import Path


class ConfigManager:
    __config = None

    def __init__(self, file_name: str | Path = None):
        """
        Loads the configuration file `file_name` and assigns it to the instance
        attribute `__config`.

        Args:
            file_name (None): name of a configuration file to be loaded by the function.

        """
        self.__config = self.load_config(file_name)

    def __getitem__(self, item):
        """
        Retrieves a configuration value from the instance's config dictionary based
        on the passed item key and returns it.

        Args:
            item (str): configuration value to be retrieved by the function.

        Returns:
            str: a configuration item value.

        """
        return self.__config[item]

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
                _data = json.load(jsonfile)
        except FileNotFoundError:
            raise RuntimeError("Unable to find config.json")
        except ValueError:
            raise RuntimeError("Not valid JSON")
        return _data
