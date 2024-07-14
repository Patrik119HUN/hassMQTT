from core.device.entity import Entity
from core.repository import *


class DeviceManager:
    def __init__(self):
        self.__light_repository = LightRepository()
        self.__sensor_repository = SensorRepository()
        self.__alarm_repository = AlarmRepository()

    def list(self) -> list[Entity]:
        yield from self.__light_repository.list()
        yield from self.__sensor_repository.list()

    def save(self, entity: Entity):
        self.__light_repository.save(entity)
        self.__sensor_repository.add(entity)

    def remove(self, unique_id: str):
        self.__light_repository.delete(unique_id)
        self.__sensor_repository.delete(unique_id)

    def get(self, unique_id: str) -> Entity:
        pass
