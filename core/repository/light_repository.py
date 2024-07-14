from core.device.entity import Entity
from core.repository.dao import HardwareDAO, DeviceDriverDAO, EntityDAO, LightDAO
from core.config_manager import config_manager
from core.device.light import BinaryLight, BrightnessLight, RGBLight
from core.device.driver.driver_factory import DriverFactory
from loguru import logger


light_registry = {"binary": BinaryLight, "brightness": BrightnessLight, "rgb": RGBLight}


class LightRepository:
    def __init__(self):
        self.__hardware_dao = HardwareDAO(config_manager["database"])
        self.__device_driver_dao = DeviceDriverDAO(config_manager["database"])
        self.__entity_dao = EntityDAO(config_manager["database"])
        self.__light_dao = LightDAO(config_manager["database"])
        self.__driver_factory = DriverFactory()

    def save(self, entity: Entity):
        if entity.entity_type != "light":
            return
        if self.__entity_dao.get(entity.unique_id) is None:
            self.__entity_dao.create(entity)
            self.__light_dao.create(entity)
            self.__device_driver_dao.create(entity)
            self.__hardware_dao.create(entity)

    def delete(self, unique_id: str):
        entity = self.__entity_dao.get(unique_id)
        if entity.entity_type != "light":
            return
        self.__entity_dao.delete(unique_id)
        self.__light_dao.delete(unique_id)
        self.__device_driver_dao.delete(unique_id)
        self.__hardware_dao.delete(unique_id)

    def list(self):
        for light in self.__light_dao.list():
            entity = self.__entity_dao.get(light["unique_id"])
            yield self.__create_light(entity, light["color_mode"])

    def get(self, unique_id: str):
        entity = self.__entity_dao.get(unique_id)
        if entity.entity_type != "light":
            return None
        color_mode = self.__light_dao.get(unique_id)["color_mode"]
        return self.__create_light(entity, color_mode)

    def __get_driver(self, unique_id: str):
        driver = self.__device_driver_dao.get(unique_id)
        return self.__driver_factory.get(
            unique_id, driver=driver["driver"], address=driver["address"]
        )

    def __create_light(self, entity: Entity, color_mode: str):
        light_class = light_registry.get(color_mode)
        light = light_class(
            name=entity.name,
            unique_id=entity.unique_id,
            hardware=entity.hardware,
            icon=entity.icon,
            entity_type="light",
        )
        light.driver = self.__get_driver(entity.unique_id)
        logger.debug(f"created an {light.__class__.__name__}")
        return light
