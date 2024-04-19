from pymodbus.client import (
    ModbusBaseClient,
    ModbusTcpClient,
    ModbusSerialClient,
    ModbusUdpClient,
)
from config_manager import ConfigManager
from utils.singleton import SingletonMeta
from loguru import logger


class ModbusManager(metaclass=SingletonMeta):
    _modbus_instance: ModbusBaseClient = None
    _cm = ConfigManager("../config.json")

    def __init__(self):
        _settings = self._cm["Modbus"]
        _type: str = _settings["type"]
        _port: int | str = _settings["port"]
        _host: str = "localhost"
        _baudrate: int = 9600
        _logging: str

        if _type == "serial":
            _baudrate = _settings["baud_rate"]
            self._modbus_instance = ModbusSerialClient(port=_port, baudrate=_baudrate)
            _logging = f"on {_port} with {_baudrate} baud!"
        elif _type == "tcp" or _type == "udp":
            _host = _settings["host"]

            self._modbus_instance = (
                ModbusTcpClient(host=_host, port=_port)
                if _type == "tcp"
                else ModbusUdpClient(host=_host, port=_port)
            )
            _logging = f"on {_host}:{_port}!"

        logger.info(f"Modbus {_type} instance is created " + _logging)
