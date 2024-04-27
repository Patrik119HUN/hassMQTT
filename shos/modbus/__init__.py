from typing import Any, Protocol
from pymodbus.client import (
    ModbusTcpClient,
    ModbusSerialClient,
    ModbusUdpClient,
)
from shos.config_manager import config_manager
from loguru import logger
from abc import ABC
from typing import Type


class BaseModbus(ABC):
    __modbus_instance = None
    __settings: dict[str, Any] = config_manager["Modbus"]

    def get_client(self):
        return self.__modbus_instance


_MODBUS: dict[str, Type[BaseModbus]] = {}


def register_modbus(modbus_type: str):
    def decorator(fn):
        _MODBUS[modbus_type] = fn
        return fn

    return decorator


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


def get_modbus():
    _type = config_manager["Modbus"]["type"]
    if _type not in _MODBUS:
        raise RuntimeError("No such a modbus type")
    return _MODBUS[_type]().get_client()
