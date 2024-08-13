from pymodbus.client.base import ModbusBaseSyncClient
from loguru import logger
from core.device.driver.abstract_driver import AbstractDriver
from core.modbus_controller import modbus_controller
from typing import Dict, Any


class DriverFactory:
    __driver_registry: Dict[str, AbstractDriver] = {}
    __modbus_manager = None

    def __init__(
        self, modbus_manager: ModbusBaseSyncClient = modbus_controller.instance
    ):
        logger.trace("DeviceFactory initialized")
        DriverFactory.__modbus_manager = modbus_manager

    @classmethod
    def register(cls, name: str, driver: AbstractDriver):
        DriverFactory.__driver_registry[name] = driver

    @classmethod
    def get(cls, driver: Any, address: int) -> AbstractDriver:
        driver = cls.__driver_registry[driver](cls.__modbus_manager)
        driver.connect(id=address)
        return driver
