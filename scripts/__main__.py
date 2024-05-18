import logging.config
from shos.config_manager import load_config
from typing import Any
from pathlib import Path
from shos.utils.modbus_factory import get_modbus
import shos.device_manager as device_manager

CONFIG_FILE = (Path(__file__).parent / "../config.json").resolve()
config_manager: dict[str, Any] = load_config(CONFIG_FILE)


def main():
    """
    Sets up logging configuration, creates a Modbus manager, connects it to the
    devices, and then creates and returns a list of devices with the desired colors.

    """
    logging.config.dictConfig(config_manager["logging"])
    modbus_manager = get_modbus(**config_manager["modbus"])
    modbus_manager.connect()

    asd: list[device_manager.Device] = []
    for x in config_manager["devices"]:
        asd.append(device_manager.Device(**x))
    device_manager.modbus_manager = modbus_manager
    dev_list = device_manager.create_devices(asd)
    light = dev_list[0]
    light.state = False


if __name__ == "__main__":
    main()
