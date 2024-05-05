import logging.config
from shos.config_manager import load_config
from typing import Any
from pathlib import Path
from shos.utils.modbus_factory import get_modbus
from shos.home_assistant.light import RGBLight

CONFIG_FILE = (Path(__file__).parent / "../config.json").resolve()
config_manager: dict[str, Any] = load_config(CONFIG_FILE)
from shos.device_manager import DeviceMaker


def main():
    logging.config.dictConfig(config_manager["logging"])
    modbus_manager = get_modbus(**config_manager["modbus"])
    modbus_manager.connect()
    maker = DeviceMaker(config_manager["devices"], modbus_manager=modbus_manager)
    maker.create_devices()
    light = maker.devices[0]
    light.color = (0, 10, 55)


if __name__ == "__main__":
    main()
