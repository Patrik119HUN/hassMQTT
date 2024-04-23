from typing import Any, Protocol
from pymodbus.client import (
    ModbusBaseClient,
    ModbusTcpClient,
    ModbusSerialClient,
    ModbusUdpClient,
)
from shos.config_manager import config_manager
from loguru import logger
from abc import ABC


class BaseModbus(ABC):
    _modbus_instance: ModbusBaseClient

    def get_client(self):
        return self._modbus_instance


_MODBUS: dict[str, BaseModbus] = {}


def register_modbus(modbus_type: str):
    def decorator(fn):
        _MODBUS[modbus_type] = fn
        return fn

    return decorator


@register_modbus(modbus_type="tcp")
class TCPModbus(BaseModbus):
    def __init__(self):
        _settings: dict[str, Any] = config_manager["Modbus"]
        _port: int = _settings.get("port", 502)
        _host: str = _settings.get("host", "localhost")
        self._modbus_instance = ModbusTcpClient(host=_host, port=_port)
        logger.info(f"TCP Modbus instance is created on {_host}:{_port}!")


@register_modbus(modbus_type="udp")
class UDPModbus(BaseModbus):
    def __init__(self):
        _settings: dict[str, Any] = config_manager["Modbus"]
        _port: int = _settings.get("port", 502)
        _host: str = _settings.get("host", "localhost")
        self._modbus_instance = ModbusUdpClient(host=_host, port=_port)
        logger.info(f"UDP Modbus instance is created on {_host}:{_port}!")


@register_modbus(modbus_type="serial")
class SerialModbus(BaseModbus):
    def __init__(self):
        _settings: dict[str, Any] = config_manager["Modbus"]
        _port: str = _settings.get("port", "/dev/ttyS0")
        _baudrate: int = _settings.get("baud_rate", 9600)
        self._modbus_instance = ModbusSerialClient(port=_port, baudrate=_baudrate)
        logger.info(
            f"Serial Modbus instance is created on {_port} with {_baudrate} baud!"
        )


def get_modbus():
    _type = config_manager["Modbus"]["type"]
    if _type not in _MODBUS:
        raise RuntimeError("No such a modbus type")
    return _MODBUS[_type]().get_client()
