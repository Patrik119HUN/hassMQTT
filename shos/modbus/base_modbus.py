from pymodbus.client.base import ModbusBaseSyncClient
from shos.config_manager import config_manager
from abc import ABC
from typing import Any


class BaseModbus(ABC):
    __modbus_instance: [ModbusBaseSyncClient] = None
    __settings: dict[str, Any] = config_manager["Modbus"]

    @property
    def settings(self):
        return self.__settings

    @property
    def instance(self):
        return self.__modbus_instance

    @instance.setter
    def instance(self, new_instance: [ModbusBaseSyncClient]):
        self.__modbus_instance = new_instance
