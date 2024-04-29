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
        __port: int = self.settings.get("port", 502)
        __host: str = self.settings.get("host", "localhost")
        self.instance = ModbusTcpClient(host=__host, port=__port)
        logger.info(f"TCP Modbus instance is created on {__host}:{__port}!")
        self.instance.connect()


@register_modbus(modbus_type="udp")
class UDPModbus(BaseModbus):
    def __init__(self):
        __port: int = self.settings.get("port", 502)
        __host: str = self.settings.get("host", "localhost")
        self.instance = ModbusUdpClient(host=__host, port=__port)
        logger.info(f"UDP Modbus instance is created on {__host}:{__port}!")
        self.instance.connect()


@register_modbus(modbus_type="serial")
class SerialModbus(BaseModbus):
    def __init__(self):
        __port: str = self.settings.get("port", "/dev/ttyS0")
        __baudrate: int = self.settings.get("baud_rate", 9600)
        self.instance = ModbusSerialClient(port=__port, baudrate=__baudrate)
        logger.info(
            f"Serial Modbus instance is created on {__port} with {__baudrate} baud!"
        )
        self.instance.connect()
