from shos.config_manager import config_manager
from typing import Any, Type
from shos.home_assistant.light import *
import json

from shos.home_assistant.light.light_factory import get_light


class DeviceMaker:
    __device_json: dict[str, Any] = config_manager.get("devices")
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


def main():
    asd = DeviceMaker()
    asd.create_devices()


if __name__ == "__main__":
    main()
