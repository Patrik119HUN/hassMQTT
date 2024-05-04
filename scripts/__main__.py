import logging.config
from shos.config_manager import load_config
from typing import Any
from pathlib import Path
from shos.utils.modbus_factory import get_modbus

CONFIG_FILE = (Path(__file__).parent / "../config.json").resolve()
config_manager: dict[str, Any] = load_config(CONFIG_FILE)


def main():
    logging.config.dictConfig(config_manager["logging"])
    modbus_manager = get_modbus(**config_manager["modbus"])
    print(modbus_manager)


if __name__ == "__main__":
    main()
