from typing import Any

from shos.home_assistant.light.driver import ModbusDriver
from shos.home_assistant.light.light_factory import get_light
from pymodbus.client import ModbusBaseClient
import logging


class DeviceMaker:
    __devices_dict: dict[str, Any] = None
    __devices: list[Any] = []
    __modbus_manager: ModbusBaseClient
    __logger = logging.getLogger(__name__)

    def __init__(self, devices: dict[str, Any], modbus_manager: ModbusBaseClient):
        self.__devices_dict = devices
        self.__modbus_manager = modbus_manager

    def create_devices(self):
        for props in self.__devices_dict:
            device = None
            match props["type"]:
                case "light":
                    device = get_light(props["color_mode"])(props["name"])
                    self.__logger.debug(f"created an {device} light")
                case "binary_sensor":
                    self.__logger.info("Not implemented yet")
                case "alarm":
                    self.__logger.info("Not implemented yet")
                case _:
                    print("none")

            match props["hardware_type"]:
                case "modbus":
                    __driver = ModbusDriver(self.__modbus_manager)
                    __driver.connect(id=1)
                case "can":
                    self.__logger.info("Not implemented yet")
                case "hat":
                    self.__logger.info("Not implemented yet")
            device.driver = __driver
            self.__devices.append(device)

    @property
    def devices(self):
        return self.__devices
