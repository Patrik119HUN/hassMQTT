from core.device.device_factory import DeviceFactory
from core.device.entity import Entity
from core.repository import (
    EntityRepository,
    DeviceDriverRepository,
    HardwareRepository,
    LightRepository,
)
from core.config_manager import config_manager
from core.device.light import BinaryLight


class DeviceManager:
    __device_list: list[Entity] = []

    def __init__(self):
        self.__entity_repository = EntityRepository(config_manager["database"])
        self.__hardware_repository = HardwareRepository(config_manager["database"])
        self.__device_driver_repository = DeviceDriverRepository(config_manager["database"])
        self.__light_repository = LightRepository(config_manager["database"])
        self.__device_factory = DeviceFactory()

    def list(self) -> list[Entity]:
        for e in self.__entity_repository.list():
            dev = self.__device_factory.get_device(
                e.entity_type, e.name, e.unique_id, e.hardware, e.icon
            )
            yield dev

    def add(self, entity: Entity):
        self.__entity_repository.create(entity)
        self.__device_driver_repository.create(entity)
        self.__hardware_repository.create(entity)
        if isinstance(entity, BinaryLight):
            self.__light_repository.create(entity)

    def remove(self, unique_id: str):
        self.__entity_repository.delete(unique_id)
        self.__device_driver_repository.delete(unique_id)
        self.__hardware_repository.delete(unique_id)
        self.__light_repository.create(unique_id)
        entity = self.get(unique_id)
        self.__device_list.remove(entity)

    def get(self, unique_id: str) -> Entity:
        for entity in self.__device_list:
            if entity.unique_id == unique_id:
                return entity
