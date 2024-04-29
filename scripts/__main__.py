import atexit
import logging.config

from shos.config_manager import load_config
from typing import Any, Type
from shos.home_assistant.light import *

from pathlib import Path
from shos.home_assistant.light.light_factory import get_light


class DeviceMaker:
    __device_json: dict[str, Any] = None #config_manager.get("devices")
    __devices: list[Any]

    def create_devices(self):
        for name, props in self.__device_json.items():
            __name: name
            __type = props.get("type")
            __class = None
            __driver: [LightDriver]
            if __type == "light":
                __class = get_light(props.get("color_mode"))

            __hardware: dict[str, Any] = props.get("hardware")
            if __hardware.get("type") == "modbus":
                __driver = driver.ModbusDriver()
                __driver.connect(id=2, light=__class(name))

    @property
    def devices(self):
        return self.__devices


settings = load_config((Path(__file__).parent / "../logging.json").resolve())

logger = logging.getLogger("alma")


def main():
    logging.config.dictConfig(settings)

    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

    logger.warning("hiba")
    # asd = DeviceMaker()
    # asd.create_devices()


if __name__ == "__main__":
    main()
