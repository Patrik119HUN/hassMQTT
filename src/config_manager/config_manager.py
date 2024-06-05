import json
from typing import Any

from pathlib import Path
from dotenv import dotenv_values


class ConfigManager:
    __config = None

    def __init__(self, file_name: str | Path = None):
        """
        Loads configuration data from a file `file_name` and assigns it to the
        instance's internal configuration variable `self.__config`.

        Args:
            file_name (None): file that contains the configuration data to be
                loaded into the `__config` attribute of the instance.

        """
        self.__config = self.load_config(file_name)

    def __getitem__(self, item):
        """
        Retrieves a value from a configuration object's item based on its key and
        returns it without modification or additional processing.

        Args:
            item (..........................): value of an item in the configuration
                dictionary that the function is processing.
                
                	The variable 'self.' represents the class that is being operated
                on by the function, while [config] refers to the config attribute
                of this class. In the expression [self.__config[item]], [item] is
                the thing being queried for information.

        Returns:
            object: the value stored for the given key in the instance's configuration
            dictionary.
            
            	The output of `__getitem__` is an instance of the `Config` class,
            which contains various attributes and methods related to the configuration
            of the application. These attributes and methods include:
            
            		- `item`: This is the item that was requested, which can be a string
            or a tuple of strings representing the configuration value.
            		- `config`: This is the dictionary containing the configuration
            values for the application.
            		- `__class__`: This is the class of the output instance, which is
            the `Config` class in this case.
            
            	Overall, the `__getitem__` function provides a convenient way to
            access and manipulate the configuration values of an application through
            the use of dictionaries and classes.

        """
        return self.__config[item]

    def load_env(self, name: str, file_name: str | Path = None):
        """
        Loads environmental variables from a dotenv file into the object
        `self.__config`. It iterates through the items in the dictionary `dotenv_values`
        and assigns each value to the corresponding property in `self.__config`
        based on the lowercase key.

        Args:
            name (str): name of the configuration variable being updated.
            file_name (None): file containing the environmental variables to be loaded.

        """
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
                _data = json.load(jsonfile)
        except FileNotFoundError:
            raise RuntimeError("Unable to find config.json")
        except ValueError:
            raise RuntimeError("Not valid JSON")
        return _data
