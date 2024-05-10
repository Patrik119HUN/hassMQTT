from typing import Any
from shos.home_assistant.binary_sensor import BinarySensor
from shos.home_assistant.light.driver import ModbusDriver
from shos.home_assistant.light.light_factory import get_light
from pymodbus.client.base import ModbusBaseSyncClient
from dataclasses import dataclass
from loguru import logger


@dataclass
class Device:
    name: str
    type: str
    color_mode: str
    device_id: int
    hardware_type: str


modbus_manager: ModbusBaseSyncClient


def create_devices(device_list: list[Device]) -> list[Any]:
    devices: list[Any] = []
    for device in device_list:
        dev = device_factory(device.type, device.name)
        driver = driver_factory(device.hardware_type)

        dev.driver = driver
        devices.append(dev)
        return devices


def device_factory(device_type: str, name: str, **kwargs):
    created_dev = None
    match device_type:
        case "light":
            created_dev = get_light(kwargs["color_mode"])(name)
        case "binary_sensor":
            created_dev = BinarySensor(name)
        case "alarm":
            raise NotImplemented("Alarm not implemented yet")
    logger.debug(f"created an {created_dev} light")
    return created_dev


def driver_factory(hardware_type: str, **kwargs):
    created_driver = None
    match hardware_type:
        case "modbus":
            created_driver = ModbusDriver(kwargs["modbus_manager"])
            created_driver.connect(id=kwargs["device_id"])
        case "can":
            raise NotImplemented("CAN driver implemented yet")
        case "hat":
            raise NotImplemented("Built in driver implemented yet")
    return created_driver
