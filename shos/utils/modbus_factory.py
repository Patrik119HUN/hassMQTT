from pymodbus.client import (ModbusSerialClient, ModbusUdpClient, ModbusTcpClient)
from pymodbus.client.base import ModbusBaseSyncClient


def get_modbus(client: str, *args, **kwargs) -> ModbusBaseSyncClient:
    modbus = {
        "serial": ModbusSerialClient,
        "udp": ModbusUdpClient,
        "tcp": ModbusTcpClient
    }
    if client not in modbus:
        raise RuntimeError("No such a modbus type")
    return modbus[client](*args, **kwargs)
