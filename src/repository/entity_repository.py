from src.repository.repository_interface import IRepository
import sqlite3
from typing import List
from src.device.entity import Entity
from src.utils.db_connect import connect
from .hardware_repository import HardwareRepository


class EntityRepository(IRepository[Entity]):
    __hardware_repo: HardwareRepository

    def __init__(self, path: str):
        super().__init__(path)
        self.__hardware_repo = HardwareRepository(path)

    def list(self) -> list[Entity]:
        entity_list: List[Entity] = []
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from entity")
            for entity in cursor.fetchall():
                hardware = self.__hardware_repo.get(entity["hardware_id"])
                entity_list.append(
                    Entity(
                        name=entity["name"],
                        hardware=hardware,
                        entity_type=entity["entity_type"],
                        icon=entity["icon"],
                        unique_id=entity["unique_id"],
                    )
                )
            return entity_list

    def get(self, item_id: int) -> Entity:
        with connect(self._path) as cursor:
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * from entity")
            entity = cursor.fetchone()
            hardware = self.__hardware_repo.get(entity["hardware_id"])
            return Entity(
                name=entity["name"],
                hardware=hardware,
                entity_type=entity["entity_type"],
                icon=entity["icon"],
                unique_id=entity["unique_id"],
            )

    def create(self, item: Entity) -> None:
        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO entity VALUES (?, ?, ?, ?, ?,?)",
                [
                    item.unique_id,
                    item.name,
                    item.driver.__class__.__name__,
                    item.entity_type,
                    1,
                    item.icon,
                ],
            )

    def update(self, item: int, *args, **kwargs) -> None:
        pass

    def delete(self, item_id: int) -> None:
        pass
