from abc import ABC, abstractmethod
from loguru import logger

from pymodbus import ModbusException
from pymodbus.client.base import ModbusBaseSyncClient


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
    __modbus: [ModbusBaseSyncClient] = None

    def __init__(self, modbus_instance: ModbusBaseSyncClient):
        self.__modbus = modbus_instance

    def connect(self, *args, **kwargs):
        if "id" not in kwargs:
            raise RuntimeError("No slave id specified")
        self.__id = kwargs["id"]
        logger.info(f"Connecting to {self.__id}")

    def disconnect(self):
        logger.info(f"Disconnecting from {self.__id}")

    def send_data(self, address: int, value: int):
        try:
            self.__modbus.write_register(address=address, value=value, slave=self.__id)
            logger.debug(f"Writing register to {self.__id} with {value} value")
        except ModbusException as e:
            logger.error(
                f"Modbus write error at id: {self.__id}, address:{address}, {e}"
            )
            raise RuntimeError(e)

    def get_data(self):
        pass
