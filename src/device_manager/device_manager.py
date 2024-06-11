from src.device.device_factory import DeviceFactory
from src.device.entity import Entity
from src.modbus_controller import modbus_controller
from src.repository import EntityRepository
from src.config_manager import config_manager


class DeviceManager:
    __device_list: list[Entity] = []
    __device_factory: DeviceFactory

    def __init__(self):
        self.__device_factory = DeviceFactory()
        for e in EntityRepository(config_manager["database"]).list():
            dev = self.__device_factory.get_device(
                e.entity_type, e.name, e.unique_id, e.hardware, e.icon
            )
            self.__device_list.append(dev)

    def list(self) -> list[Entity]:
        return self.__device_list

    def add(self, entity: Entity):
        self.__device_list.append(entity)

    def remove(self, unique_id: str):
        entity = self.get(unique_id)
        self.__device_list.remove(entity)

    def get(self, unique_id: str) -> Entity:
        for entity in self.__device_list:
            if entity.unique_id == unique_id:
                return entity
