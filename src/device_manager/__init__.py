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
        """
        Sets up a Modbus manager object, which can communicate with Modbus devices
        and perform various tasks.

        Args:
            modbus_driver (instance of `modbus.ModBusDriver`.): Modbus driver to
                use for communicating with the Modbus device.
                
                		- `self.__modbus_manager`: This is an instance of the `ModBusManager`
                class, which is used to manage the Modbus communication.

        """
        self.__modbus_manager = modbus_driver

    def create_device(self, device: Device) -> Entity:
        """
        Creates a new device object and assigns it a driver object, returning the
        device object.

        Args:
            device (Device): device object that is being created and assigned a
                driver instance.

        Returns:
            Entity: a device object with a reference to the associated driver.

        """
        dev = DeviceManager.device_factory(**asdict(device))
        driver = self.driver_factory(**asdict(device))

        dev.driver = driver
        return dev

    @staticmethod
    def device_factory(device_type: str, name: str, **kwargs) -> Entity:
        """
        Creates a device instance based on a user-provided `device_type`. It uses
        the `get_light` function to create a `Light` object if `device_type` is
        "light", and the `BinarySensor` class to create a `BinarySensor` object
        if `device_type` is "binary_sensor". If `device_type` is "alarm", it raises
        a `NotImplemented` error.

        Args:
            device_type (str): type of device to be created, which determines the
                specific implementation class used to create the device.
            name (str): name of the device to be created, which is used to create
                an instance of the appropriate class in the `created_dev` variable.

        Returns:
            Entity: an instance of a device class depending on the input `device_type`.

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
        """
        Checks if a device type is already registered in the device registry. If
        it is, it replaces it with the passed-in wrapped class.

        Args:
            cls (unspecified type object/module/namespace.): current class in which
                the function is defined, and is used to check if a device type
                already exists in the class's device registry.
                
                	1/ `device_registry`: a dict-like object containing registered
                device types and their associated classes.
                	2/ `name`: a str or tuple of str representing the unique identifier
                for a device type.
                	3/ `logger`: an instance of `logging.Logger` used for warning
                messages related to duplicate device registrations.
            name (str): name of the device type that is being passed to the function
                for wrapping.

        Returns:
            Callable: a callable object that replaces an existing device in the
            registry if it exists.

        """
        def inner_wrapper(wrapped_class) -> Callable:
            """
            Replaces an existing device type in the registry with a wrapped version
            of it, preserving its original name.

            Args:
                wrapped_class (object of class.): 3rd-party class that will be
                    wrapped with additional functionality by the `DeviceWrapping`
                    class, and is passed to the function for wrapping.
                    
                    		- `name`: The name of the device type (string).
                    		- `device_registry`: A dictionary of device types (string,
                    optional).

            Returns:
                Callable: a warning message indicating that a device type already
                exists and will be replaced with the new wrapping class.

            """
            if name in cls.device_registry:
                logger.warning(
                    f"Device type {name} is already exists. Will replace it."
                )
                cls.device_registry[name] = wrapped_class
                return wrapped_class

        return inner_wrapper

    @classmethod
    def create_device(cls, name: str, **kwargs):
        """
        Verifies if a given device name exists in the class's device registry, and
        if not, logs a warning message. If the device exists, it returns a reference
        to the device object in the registry.

        Args:
            cls ("Instance of 'DeviceType'".): device registry in which the function
                is searching for the specified `name`.
                
                		- `device_registry`: a dictionary containing a list of device
                types and their corresponding Python classes for deserialization.
            name (str): identifier of the device to check its existence in the `device_registry`.

        Returns:
            str: a reference to a Device object if the device exists in the device
            registry, or `None` otherwise.

        """
        if name not in cls.device_registry:
            logger.warning(f"{name} type of device not exists.")
            return None
        return cls.device_registry[name]
