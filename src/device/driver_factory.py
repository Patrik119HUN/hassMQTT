from pymodbus.client.base import ModbusBaseSyncClient
from src.home_assistant.driver.modbus_driver import ModbusDriver
from loguru import logger
from src.repository import DeviceDriverRepository
from src.config_manager import config_manager
from src.home_assistant.driver.abstract_driver import AbstractDriver
from src.modbus_controller import modbus_controller


class DriverFactory:
    __device_driver_repository: DeviceDriverRepository = None
    __modbus_manager: ModbusBaseSyncClient = None
    __driver_registry = {"modbus": ModbusDriver, "can": None, "hat": None}

    def __init__(self, modbus_manager: ModbusBaseSyncClient = modbus_controller.instance):
        logger.trace("DeviceFactory initialized")
        self.__device_driver_repository = DeviceDriverRepository(config_manager["database"])
        self.__modbus_manager = modbus_manager

    def get(self, unique_id: str) -> AbstractDriver:
        params = self.__device_driver_repository.get(unique_id)
        driver = self.__driver_registry[params["driver"]](self.__modbus_manager)
        driver.connect(id=params["address"])
        return driver
