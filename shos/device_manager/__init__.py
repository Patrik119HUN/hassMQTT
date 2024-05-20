from typing import Any
from shos.home_assistant.binary_sensor import BinarySensor
from shos.home_assistant.light.driver import ModbusDriver
from shos.home_assistant.light.light_factory import get_light
from pymodbus.client.base import ModbusBaseSyncClient
from dataclasses import dataclass, asdict
from loguru import logger


@dataclass
class Device:
    name: str
    device_type: str
    color_mode: str
    device_id: int
    hardware_type: str


modbus_manager: ModbusBaseSyncClient


def create_devices(device_list: list[Device]) -> list[Any]:
    """
    Takes a list of device definitions and returns a list of Device objects, each
    with a reference to a driver object.

    Args:
        device_list (list[Device]): list of devices for which drivers are to be generated.

    Returns:
        list[Any]: a list of device objects, each with a corresponding hardware
        driver object.

    """
    devices: list[Any] = []
    for device in device_list:
        dev = device_factory(**asdict(device))
        driver = driver_factory(**asdict(device))

        dev.driver = driver
        devices.append(dev)
        return devices


def device_factory(device_type: str, name: str, **kwargs):
    """
    Creates a device based on the `device_type` parameter passed as part of the
    keyword arguments, and returns it.

    Args:
        device_type (str): type of device to create, which determines the specific
            instance of the `Light`, `BinarySensor`, or `Alarm` class to generate
            based on its value.
        name (str): name of the device to be created, and it is used as the name
            of the newly generated device object in the `created_dev` variable.

    Returns:
        BinarySensor: a light object that represents a newly created device with
        the given name and color mode.
        
        		- `created_dev`: The type of device created, which is determined by the
        value of `device_type`.
        		- `name`: A unique name assigned to the device.

    """
    created_dev = None
    match device_type:
        case "light":
            created_dev = get_light(kwargs["color_mode"])(name)
        case "binary_sensor":
            created_dev = BinarySensor(name)
        case "alarm":
            raise NotImplemented("Alarm not implemented yet")
    logger.debug(f"created an {created_dev.__class__.__name__}")
    return created_dev


def driver_factory(hardware_type: str, **kwargs):
    """
    Creates a driver instance for a given hardware type based on user-provided
    parameters. The function supports Modbus, CAN and Built-in drivers. For
    unsupported hardware types, the function raises a `NotImplemented` error.

    Args:
        hardware_type (str): type of hardware being controlled, and the function
            returns a corresponding driver instance depending on the value provided.

    Returns:
        instance of the `ModbusDriver` class: a Modbus driver instance for devices
        of the `modbus` hardware type.
        
        		- `created_driver`: The created driver instance, which is an object of
        type `ModbusDriver` if the hardware type is "modbus", and otherwise raises
        a `NotImplemented` error.

    """
    created_driver = None
    match hardware_type:
        case "modbus":
            created_driver = ModbusDriver(modbus_manager)
            created_driver.connect(id=kwargs["device_id"])
        case "can":
            raise NotImplemented("CAN driver implemented yet")
        case "hat":
            raise NotImplemented("Built in driver implemented yet")
    return created_driver
