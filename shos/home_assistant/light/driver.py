from loguru import logger

from pymodbus import ModbusException
from pymodbus.client.base import ModbusBaseSyncClient
from shos.home_assistant.abstract_driver import AbstractDriver


class ModbusDriver(AbstractDriver):
    __id: int = 0
    __modbus: [ModbusBaseSyncClient] = None

    def __init__(self, modbus_instance: ModbusBaseSyncClient):
        self.__modbus = modbus_instance

    def connect(self, *args, **kwargs):
        """
        Establishes a connection to a slave device with the specified ID using the
        provided logger for error messages and updates the instance variable `id`
        with the received ID.

        """
        if "id" not in kwargs:
            raise RuntimeError("No slave id specified")
        self.__id = kwargs["id"]
        logger.info(f"Connecting to {self.__id}")

    def disconnect(self):
        logger.info(f"Disconnecting from {self.__id}")

    def send_data(self, address: int, value: int):
        """
        Writes a value to a specific register on a Modbus device using the specified
        address and slave ID.

        Args:
            address (int): 16-bit address of the register to be written on the
                Modbus device.
            value (int): 16-bit value to be written to the Modbus register.

        """
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
