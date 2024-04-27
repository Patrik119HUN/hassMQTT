from pymodbus.client.base import ModbusBaseSyncClient
from shos.config_manager import config_manager
from abc import ABC
from typing import Any


class BaseModbus(ABC):
    __modbus_instance: [ModbusBaseSyncClient] = None
    __settings: dict[str, Any] = config_manager["Modbus"]

    @property
    def client(self):
        return self.__modbus_instance
