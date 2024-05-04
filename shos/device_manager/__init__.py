from typing import Any

from shos.home_assistant.light.driver import ModbusDriver
from shos.home_assistant.light.light_factory import get_light
from shos.modbus import BaseModbus
import logging


class DeviceMaker:
    __devices_dict: dict[str, Any] = None
    __devices: list[Any]
    __modbus_manager: BaseModbus
    __logger = logging.getLogger(__name__)

    def __init__(self, devices: dict[str, Any]):
        self.__devices_dict = devices

    def create_devices(self):
        for name, props in self.__devices_dict.items():
            device = None
            match props["type"]:
                case "light":
                    device = get_light(props["color_mode"])
                case "binary_sensor":
                    self.__logger.info("Not implemented yet")
                case "alarm":
                    self.__logger.info("Not implemented yet")
                case _:
                    print("none")

            hardware: dict[str, Any] = props["hardware"]
            match hardware["type"]:
                case "modbus":
                    __driver = ModbusDriver(self.__modbus_manager)
                    __driver.connect(id=2, light=device(name))
                case "can":
                    self.__logger.info("Not implemented yet")
                case "hat":
                    self.__logger.info("Not implemented yet")

    @property
    def devices(self):
        return self.__devices
