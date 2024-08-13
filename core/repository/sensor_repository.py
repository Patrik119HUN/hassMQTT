from core.device.entity import Entity
from core.config_manager import config_manager
from core.device.binary_sensor import BinarySensor
from core.repository.dao import HardwareDAO, DeviceDriverDAO, EntityDAO, LightDAO
from core.device.driver.gpio_driver import GPIODriver, PinType
from loguru import logger
from typing import List


class SensorRepository:
    def __init__(self):
        self.__hardware_dao = HardwareDAO(config_manager["database"])
        self.__device_driver_dao = DeviceDriverDAO(config_manager["database"])
        self.__entity_dao = EntityDAO(config_manager["database"])

    def add(self, entity: Entity):
        if entity.entity_type != "sensor":
            return
        self.__entity_dao.create(entity)
        self.__device_driver_dao.create(entity)
        self.__hardware_dao.create(entity)

    def delete(self, unique_id: str):
        entity = self.__entity_dao.get(unique_id)
        if entity.entity_type != "sensor":
            return
        self.__entity_dao.delete(unique_id)
        self.__device_driver_dao.delete(unique_id)
        self.__hardware_dao.delete(unique_id)

    def list(self) -> List[BinarySensor]:
        sensor_list: List[BinarySensor] = []
        for entity in self.__entity_dao.list():
            if entity.entity_type == "sensor":
                driver = self.__get_driver(entity.unique_id)
                sensor_list.append(SensorRepository.create_sensor(entity, driver))
        return sensor_list

    def get(self, unique_id: str):
        entity = self.__entity_dao.get(unique_id)
        if entity.entity_type == "sensor":
            driver = self.__get_driver(entity.unique_id)
            return SensorRepository.create_sensor(entity, driver)
        return None

    def update(self, entity: Entity):
        pass

    def __get_driver(self, unique_id: str):
        driver_data = self.__device_driver_dao.get(unique_id)
        gpio_driver = GPIODriver()
        gpio_driver.connect(pin=driver_data["address"], type=PinType.INPUT)
        return gpio_driver

    @classmethod
    def create_sensor(self, entity: Entity, driver):
        sensor = BinarySensor(
            name=entity.name,
            unique_id=entity.unique_id,
            hardware=entity.hardware,
            icon=entity.icon,
            entity_type="binary_sensor",
            driver=driver,
        )
        logger.debug(f"created an {sensor.__class__.__name__}")
        return sensor
