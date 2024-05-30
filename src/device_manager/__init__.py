from typing import Any, Callable
from src.home_assistant.binary_sensor import BinarySensor
from src.home_assistant.light.driver import ModbusDriver
from src.home_assistant.light.light_factory import get_light
from pymodbus.client.base import ModbusBaseSyncClient
from dataclasses import dataclass, asdict
from loguru import logger
from src.home_assistant.device import Entity
from src.modbus_controller import modbus_controller
from src.config_manager import config_manager


@dataclass
class Device:
    name: str
    device_type: str
    color_mode: str
    device_id: int
    hardware_type: str


class DeviceManager:
    __modbus_manager: ModbusBaseSyncClient = None

    def __init__(self, modbus_driver=modbus_controller.instance):
        self.__modbus_manager = modbus_driver

    def create_device(self, device: Device) -> Entity:
        dev = DeviceManager.device_factory(**asdict(device))
        driver = self.driver_factory(**asdict(device))

        dev.driver = driver
        return dev

    @staticmethod
    def device_factory(device_type: str, name: str, **kwargs) -> Entity:
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

    def driver_factory(self, hardware_type: str, **kwargs):
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
                created_driver = ModbusDriver(self.__modbus_manager)
                created_driver.connect(id=kwargs["device_id"])
            case "can":
                raise NotImplemented("CAN driver implemented yet")
            case "hat":
                raise NotImplemented("Built in driver implemented yet")
        return created_driver


class DeviceFactory:
    device_registry = {}

    @classmethod
    def register_device(cls, name: str) -> Callable:
        def inner_wrapper(wrapped_class) -> Callable:
            if name in cls.device_registry:
                logger.warning(
                    f"Device type {name} is already exists. Will replace it."
                )
                cls.device_registry[name] = wrapped_class
                return wrapped_class

        return inner_wrapper

    @classmethod
    def create_device(cls, name: str, **kwargs):
        if name not in cls.device_registry:
            logger.warning(f"{name} type of device not exists.")
            return None
        return cls.device_registry[name]
