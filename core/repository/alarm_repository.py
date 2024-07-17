from core.device.entity import Entity
from core.config_manager import config_manager
from core.device.binary_sensor import BinarySensor
from core.repository.dao import HardwareDAO, DeviceDriverDAO, EntityDAO, LightDAO

class AlarmRepository:
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

    def list(self):
        for entity in self.__entity_dao.list():
            if entity.entity_type == "sensor":
                yield BinarySensor(
                    name=entity.name,
                    unique_id=entity.unique_id,
                    hardware=entity.hardware,
                    icon=entity.icon,
                    entity_type="binary_sensor",
                )

    def get(self, unique_id: str):
        entity = self.__entity_dao.get(unique_id)
        if entity.entity_type == "sensor":
            return BinarySensor(
                name=entity.name,
                unique_id=entity.unique_id,
                hardware=entity.hardware,
                icon=entity.icon,
                entity_type="sensor",
            )
        return None

    def update(self, entity: Entity):
        pass
