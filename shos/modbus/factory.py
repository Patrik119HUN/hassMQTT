from pymodbus.client.base import ModbusBaseSyncClient

from shos.config_manager import config_manager
from shos.modbus.base_modbus import BaseModbus

_MODBUS: dict[str, [BaseModbus]] = {}


def register_modbus(modbus_type: str):
    def decorator(fn):
        _MODBUS[modbus_type] = fn
        return fn

    return decorator


def get_modbus() -> [ModbusBaseSyncClient]:
    _type = config_manager["Modbus"]["type"]
    if _type not in _MODBUS:
        raise RuntimeError("No such a modbus type")
    return _MODBUS[_type]().get_client()
