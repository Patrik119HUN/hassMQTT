from core.device.entity import Entity
from core.repository.dao import HardwareDAO, DeviceDriverDAO, EntityDAO, LightDAO
from core.config_manager import config_manager
from core.device.light import BinaryLight, BrightnessLight, RGBLight
from loguru import logger
from typing import Any, List
from core.device.driver import DriverFactory

light_registry = {"binary": BinaryLight, "brightness": BrightnessLight, "rgb": RGBLight}


class LightRepository:
    def __init__(self):
        self.__hardware_dao = HardwareDAO(config_manager["database"])
        self.__device_driver_dao = DeviceDriverDAO(config_manager["database"])
        self.__entity_dao = EntityDAO(config_manager["database"])
        self.__light_dao = LightDAO(config_manager["database"])

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

    def list(self) -> List[BinaryLight]:
        light_list: List[BinaryLight] = []
        for light in self.__light_dao.list():
            entity = self.__entity_dao.get(light["unique_id"])
            params = self.__device_driver_dao.get(light["unique_id"])
            driver = DriverFactory.get(params["driver"], params["address"])
            light_list.append(
                LightRepository.create_light(entity, light["color_mode"], driver)
            )
        return light_list

    def get(self, unique_id: str):
        entity = self.__entity_dao.get(unique_id)
        if entity.entity_type != "light":
            return None
        color_mode = self.__light_dao.get(unique_id)["color_mode"]
        params = self.__device_driver_dao.get(unique_id)
        driver = DriverFactory.get(params["driver"], params["address"])
        return LightRepository.create_light(entity, color_mode, driver)

    @classmethod
    def create_light(cls, entity: Entity, color_mode: str, driver: Any):
        light_class = light_registry.get(color_mode)
        light = light_class(
            name=entity.name,
            unique_id=entity.unique_id,
            hardware=entity.hardware,
            icon=entity.icon,
            driver=driver,
        )
        logger.debug(f"created an {light.__class__.__name__}")
        return light
