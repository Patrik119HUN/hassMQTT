from abc import ABC, abstractmethod
from loguru import logger
import time

from pymodbus import ModbusException
from pymodbus.client.base import ModbusBaseSyncClient

from shos.modbus import get_modbus


class LightDriver(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send_data(self, address: int, value: int):
        pass

    @abstractmethod
    def get_data(self):
        pass


class ModbusDriver(LightDriver):
    __id: int = 0
    __modbus: [ModbusBaseSyncClient] = get_modbus()

    def connect(self, *args, **kwargs):
        if "id" not in kwargs:
            raise RuntimeError("No device id specified")
        self.__id = kwargs["id"]
        logger.info(f"Connecting to {self.__id}")
        time.sleep(1)
        logger.info(f"Succesfully connected")

    def disconnect(self):
        logger.info(f"Disconnecting from {self.__id}")

    def send_data(self, address: int, value: int):
        try:
            self.__modbus.write_register(address=address, value=value, slave=self.__id)
        except ModbusException as e:
            logger.error(f"Modbus write error at id: {self.__id}, address:{address}, {e}")
            raise RuntimeError(e)

    def get_data(self):
        pass
