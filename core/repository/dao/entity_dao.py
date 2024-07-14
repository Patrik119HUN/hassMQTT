from .dao_interface import DAOInterface
import sqlite3
from typing import List
from core.device.entity import Entity
from core.utils.db_connect import connect
from .hardware_dao import HardwareDAO


class EntityDAO(DAOInterface[Entity]):
    def __init__(self, path: str):
        super().__init__(path)
        self.__hardware_repo: HardwareDAO = HardwareDAO(path)

    def list(self) -> list[Entity]:
        entity_list: List[Entity] = []
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from entity")
            for entity in cursor.fetchall():
                hardware = self.__hardware_repo.get(entity["unique_id"])
                entity_list.append(Entity(**entity, hardware=hardware))
            return entity_list

    def get(self, item_id: str) -> Entity | None:
        with connect(self._path) as cursor:
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * from entity WHERE unique_id=?", [item_id])
            entity = cursor.fetchone()
            if entity is None:
                return None
            hardware = self.__hardware_repo.get(entity["unique_id"])
            return Entity(**entity, hardware=hardware)

    def create(self, item: Entity) -> None:
        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO entity VALUES (?, ?, ?, ?)",
                [
                    item.unique_id,
                    item.name,
                    item.entity_type,
                    item.icon,
                ],
            )

    def update(self, item: Entity, unique_id: str = None) -> None:
        if unique_id is None:
            unique_id = item.unique_id
        with connect(self._path) as cursor:
            cursor.execute(
                "UPDATE entity SET name=?, entity_type=?, icon=?WHERE unique_id=?",
                [item.name, item.entity_type, item.icon, unique_id],
            )
            return cursor.rowcount > 0

    def delete(self, unique_id: str) -> None:
        with connect(self._path) as cursor:
            cursor.execute("DELETE FROM entity WHERE unique_id=?", [unique_id])
            return cursor.rowcount > 0
