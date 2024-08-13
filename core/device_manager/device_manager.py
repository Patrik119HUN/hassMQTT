from core.device.entity import Entity
from core.repository import *
from typing import Generator, List
from itertools import chain


class DeviceManager:
    def __init__(self):
        self.__light_repository = LightRepository()
        self.__sensor_repository = SensorRepository()
        self.__alarm_repository = AlarmRepository()
        self.device_cache: List[Entity] = list(
            chain(self.__light_repository.list(), self.__sensor_repository.list())
        )

    def list(self) -> List[Entity]:
        return self.device_cache

    def save(self, entity: Entity):
        self.__light_repository.save(entity)
        self.__sensor_repository.add(entity)

    def remove(self, unique_id: str):
        self.__light_repository.delete(unique_id)
        self.__sensor_repository.delete(unique_id)

    def get(self, unique_id: str) -> Entity:
        pass
