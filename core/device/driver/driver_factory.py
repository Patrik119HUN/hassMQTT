from pymodbus.client.base import ModbusBaseSyncClient
from core.device.driver.modbus_driver import ModbusDriver
from loguru import logger
from core.repository import DeviceDriverRepository
from core.config_manager import config_manager
from core.device.driver.abstract_driver import AbstractDriver
from core.modbus_controller import modbus_controller


class DriverFactory:
    __device_driver_repository: DeviceDriverRepository = None
    __modbus_manager: ModbusBaseSyncClient = None
    __driver_registry = {"ModbusDriver": ModbusDriver, "can": None, "hat": None}

    def __init__(self, modbus_manager: ModbusBaseSyncClient = modbus_controller.instance):
        logger.trace("DeviceFactory initialized")
        self.__device_driver_repository = DeviceDriverRepository(config_manager["database"])
        self.__modbus_manager = modbus_manager

    def get(self, unique_id: str, **kwargs) -> AbstractDriver:
        params = self.__device_driver_repository.get(unique_id)
        driver_type = kwargs.get("driver", params["driver"])
        driver = self.__driver_registry[driver_type](self.__modbus_manager)
        driver.connect(id=kwargs.get("address", params["address"]))
        return driver
