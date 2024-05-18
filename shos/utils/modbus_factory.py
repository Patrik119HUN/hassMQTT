from pymodbus.client import (ModbusSerialClient, ModbusUdpClient, ModbusTcpClient)
from pymodbus.client.base import ModbusBaseSyncClient


def get_modbus(client: str, *args, **kwargs) -> ModbusBaseSyncClient:
    """
    Returns a client object based on the input `client` and performs actions accordingly.

    Args:
        client (str): Modbus communication type, which is either `ModbusSerialClient`,
            `ModbusUdpClient`, or `ModbusTcpClient`.

    Returns:
        ModbusBaseSyncClient: a modular client object for a specific modbus protocol
        (serial, UDP, or TCP).

    """
    modbus = {
        "serial": ModbusSerialClient,
        "udp": ModbusUdpClient,
        "tcp": ModbusTcpClient
    }
    if client not in modbus:
        raise RuntimeError("No such a modbus type")
    return modbus[client](*args, **kwargs)
