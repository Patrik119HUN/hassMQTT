from pymodbus.client import ModbusSerialClient, ModbusUdpClient, ModbusTcpClient
from pymodbus.client.base import ModbusBaseSyncClient
from src.config_manager import config_manager


class ModbusController:
    __modbus_registry = {
        "serial": ModbusSerialClient,
        "udp": ModbusUdpClient,
        "tcp": ModbusTcpClient,
    }
    __modbus_instance: ModbusBaseSyncClient = None

    def __init__(self):
        self.__modbus_instance = self.__get_modbus(**config_manager["modbus"])

    @property
    def instance(self):
        return self.__modbus_instance

    @classmethod
    def __get_modbus(cls, client: str, *args, **kwargs) -> ModbusBaseSyncClient:
        """
        Returns a client object based on the input `client` and performs actions accordingly.

        Args:
            client (str): Modbus communication type, which is either `ModbusSerialClient`,
                `ModbusUdpClient`, or `ModbusTcpClient`.

        Returns:
            ModbusBaseSyncClient: a modular client object for a specific modbus protocol
            (serial, UDP, or TCP).

        """
        if client not in ModbusController.__modbus_registry:
            raise RuntimeError("No such a modbus type")
        return ModbusController.__modbus_registry[client](*args, **kwargs)
