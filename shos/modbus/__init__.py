from pymodbus.client import (
    ModbusTcpClient,
    ModbusSerialClient,
    ModbusUdpClient,
)
from loguru import logger
from shos.modbus.factory import register_modbus
from shos.modbus.base_modbus import BaseModbus


@register_modbus(modbus_type="tcp")
class TCPModbus(BaseModbus):
    def __init__(self):
        __port: int = self.__settings.get("port", 502)
        __host: str = self.__settings.get("host", "localhost")
        self.__modbus_instance = ModbusTcpClient(host=__host, port=__port)
        logger.info(f"TCP Modbus instance is created on {__host}:{__port}!")
        self.__modbus_instance.connect()


@register_modbus(modbus_type="udp")
class UDPModbus(BaseModbus):
    def __init__(self):
        __port: int = self.__settings.get("port", 502)
        __host: str = self.__settings.get("host", "localhost")
        self._modbus_instance = ModbusUdpClient(host=__host, port=__port)
        logger.info(f"UDP Modbus instance is created on {__host}:{__port}!")
        self.__modbus_instance.connect()


@register_modbus(modbus_type="serial")
class SerialModbus(BaseModbus):
    def __init__(self):
        __port: str = self.__settings.get("port", "/dev/ttyS0")
        __baudrate: int = self.__settings.get("baud_rate", 9600)
        self._modbus_instance = ModbusSerialClient(port=__port, baudrate=__baudrate)
        logger.info(
            f"Serial Modbus instance is created on {__port} with {__baudrate} baud!"
        )
        self.__modbus_instance.connect()
